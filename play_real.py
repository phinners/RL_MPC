import time

import numpy as np

from camera_librealsense import Camera
from common_real import get_args
from env_ext_real import make_env
from envs_real import register_custom_envs
from franka_robot import FrankaRobot
from mpc_real import MPCDebugPlot
from policies_real import Policy, make_policy


class Player:
    policy: Policy = None
    debug_plot: MPCDebugPlot = None
    # debug_plot: MPCDebugPlotSmall = None
    mpc_policy = False

    obst_sizes = {"FrankaPickDynSqrObstacles-v1": np.array([[0.015, 0.017, 0.015], [0.015, 0.017, 0.015]]),
                  "FrankaPickDynObstacles-v1": np.array([[0.045, 0.017, 0.015], [0.015, 0.017, 0.015]]),
                  "FrankaPickDynObstacles-v2": np.array([[0.045, 0.017, 0.015], [0.015, 0.017, 0.015]]),
                  "FrankaPickDynLiftedObstacles-v1": np.array(
                      [[0.045, 0.017, 0.02], [0.015, 0.017, 0.02], [0.24, 0.03, 0.025]])}

    obst_vels = {"FrankaPickDynSqrObstacles-v1": np.array([0.02, 0.03]),
                 "FrankaPickDynObstacles-v1": np.array([0.0, 0.03]),
                 "FrankaPickDynObstacles-v2": np.array([0.02, 0.03]),
                 "FrankaPickDynLiftedObstacles-v1": np.array([0.02, 0.03, 0.0])}

    def __init__(self, args):
        # mujoco env set
        self.env = make_env(args)
        # policy set
        self.policy = make_policy(args)
        self.policy.set_env(env=self.env)
        # robot set
        self.robot = FrankaRobot("192.168.5.12")
        self.gripper = self.robot.gripper
        self.block_z = False if args.env == 'FrankaPickDynLiftedObstacles-v1' else True
        # real env set
        self.offset = np.array([0.8, 0.75, 0.4])  # robot base relative to the origin in simulator
        self.goal = np.array([0.5 - 0.07, -0.3, 0.0]) + self.offset
        # self.subgoal = self.goal
        if self.block_z:
            self.init = np.array([0.5, 0.3, 0.065 + 0.09])  # for FrankaPickDynLiftedObstacles-v1
            self.obst_rel_robot = np.array([[0.5, 0.1, 0.02], [0.5, -0.1, 0.05 + 0.02],
                                            [0.5, -0.1, 0.025]])  # middle pose relative to robot base
            self.z_offset = 0.00 - 0.065 - 0.09
        else:
            self.init = np.array([0.5, 0.3, 0.15])
            self.obst_rel_robot = np.array([[0.5, 0.1, 0.15], [0.5, -0.1, 0.15]])  # middle pose relative to robot base

        self.pre_dists = np.array([None, None])
        self.signs = np.array([1, 1])
        self.dt = 0.5  # time interval in real env
        self.length = 80  # number of steps to take
        self.obst_size = self.obst_sizes[args.env]  # (x/2, y/2)
        self.vels = self.obst_vels[args.env]  # velocity of obstacle
        self.pos_dif = 0.1
        self.center_x = 0.5 + self.offset[0]
        self.origin_offset = np.array([0.042, 0.038])
        # camera set
        self.camera = Camera()

    def initialize(self):
        # start camera
        self.camera.start()
        # move robot to initial pose
        self.robot.move([0, 0, 0.2])
        pose = self.robot.current_pose()[:3]
        pose[:2] = self.init[:2]
        self.robot.move_to_init(pose)
        self.gripper.move(0.05)
        input("Enter to lower the gripper.")
        if self.block_z:
            pose[2] = 0.065
        else:
            pose[2] = 0.0065
        self.robot.move_to_init(pose)
        input("Enter to grasp the object.")
        self.robot.clamp()
        self.robot.move_to_init(self.init)
        input("Enter to start moving.")

    def get_obs_distance(self):
        frame = self.camera.get_frame()
        try:
            dists, _ = self.camera.get_distance(frame, add_to_frame=False)
        except:
            dists = self.origin_offset
        dists -= self.origin_offset  # relative to origin
        return dists

    def get_obs_pose(self, dists):
        # get obstacle pose
        dyn_obstacles = []
        for i in range(len(dists)):
            dyn_obstacle = np.append(self.obst_rel_robot[i] + self.offset, self.obst_size[i])
            dyn_obstacle[0] += dists[i] - self.pos_dif
            dyn_obstacles.append(dyn_obstacle)
        return np.array(dyn_obstacles)

    def finish(self):
        self.camera.stop()
        cur_pose = self.robot.current_pose()
        if self.block_z:
            disp_z = cur_pose[2] - 0.065
        else:
            disp_z = cur_pose[2] - 0.0065
        self.robot.move([0, 0, -disp_z])
        self.robot.release()

    def close_to_goal(self, xinit):
        # cur_pos = self.robot.current_pose()[:2]
        goal = self.goal
        if np.linalg.norm(xinit[:2] - goal[:2], 2) <= 0.02:
            return True
        return False

    def play(self):
        xinit = self.init + self.offset
        cur_joint_pose, cur_joint_vel = self.robot.current_joint_state()
        dists = self.get_obs_distance()
        ob = self.env.reset()
        # print("original obs", ob)
        ob = self.set_obs(ob, xinit, dists, cur_joint_pose, cur_joint_vel)
        if args.play_policy in ['MPCPolicy']:
            self.policy.set_sub_goal(ob['desired_goal'])

        while not self.close_to_goal(xinit):
            # print("xinit: ", xinit)
            # print('ob', ob)
            t1 = time.time()
            # print("observation", ob["observation"])
            real_actions = self.policy.predict([ob])
            real_action = real_actions[0]
            if args.play_policy in ['RLPolicy']:
                real_action *= 0.05
                # for xy motion
                real_action[2] = 0
            self.robot.move(real_action[:3])
            print("action:", real_action)

            # update the original pose
            cur_pose = self.robot.current_pose()
            cur_joint_pose, cur_joint_vel = self.robot.current_joint_state()
            x_init = cur_pose[0] + self.offset[0]
            y_init = cur_pose[1] + self.offset[1]
            if self.block_z:
                z_init = ob['observation'][2]
            else:
                z_init = cur_pose[2] + self.offset[2]
            xinit = np.array([x_init, y_init, z_init])
            # print("xinit", xinit)
            dists = self.get_obs_distance()
            ob = self.set_obs(ob, xinit, dists, cur_joint_pose, cur_joint_vel)
            t2 = time.time() - t1
            print("time:", t2)
            if self.dt - t2 > 0:
                time.sleep(self.dt - t2)
        self.finish()

    def set_obs(self, obs, xinit, dists, joint_pose, joint_vel):
        obs["observation"][0:3] = xinit  # EEF POS Originally just :2
        obs["observation"][3:7] = obs["observation"][3:7]  # EEF ROT
        obs["observation"][7:14] = joint_pose  # Joint Position
        obs["observation"][16:23] = joint_vel  # Joint Velocities

        obs["observation"][25:28] = xinit  # Object Position
        obs["observation"][28:31] = obs["observation"][28:31]  # Object Relative Position

        dyn_obstacles = self.get_obs_pose(dists)

        # Obstacle 0
        obs["observation"][47:50] = dyn_obstacles[0]  # OBS0 Position
        obs["observation"][50:54] = obs["observation"][50:54]  # OBS0 Rotation
        obs["observation"][54:57] = obs["observation"][54:57]  # OBS0 Dimension

        # Obstacle 1
        obs["observation"][57:60] = dyn_obstacles[1]  # OBS1 Position
        obs["observation"][60:64] = obs["observation"][60:64]  # OBS1 Rotation
        obs["observation"][64:67] = obs["observation"][64:67]  # OBS1 Dimension

        # Obstacle 2
        obs["observation"][67:70] = obs["observation"][67:70]  # OBS2 Position
        obs["observation"][70:74] = obs["observation"][70:74]  # OBS2 Rotation
        obs["observation"][74:77] = obs["observation"][74:77]  # OBS2 Dimension

        obs["real_obstacle_info"][0, :2] = dyn_obstacles[0, :2]
        obs["real_obstacle_info"][1, :2] = dyn_obstacles[1, :2]

        if self.pre_dists.any():
            signs = np.sign(dists - self.pre_dists)
            self.signs[0] = signs[0] if signs[0] != 0 else -self.signs[0]
            self.signs[1] = signs[1] if signs[1] != 0 else -self.signs[1]
        self.pre_dists = dists

        # Obstacle 0..2 Velocity
        obs["observation"][77:80] = obs["observation"][77:80]  # OBS0 Velocity
        obs["observation"][77] = self.vels[0] * self.signs[0]  # OBS0 X Velocity

        obs["observation"][80:83] = obs["observation"][80:83]  # OBS1 Velocity
        obs["observation"][80] = self.vels[1] * self.signs[1]  # OBS1 X Velocity

        obs["observation"][83:86] = obs["observation"][83:86]  # OBS2 Velocity

        obs["obj_vels"][0, 0] = self.vels[0] * self.signs[0]
        obs["obj_vels"][1, 0] = self.vels[1] * self.signs[1]

        goal = self.goal
        obs["desired_goal"][:2] = goal[:2]

        if self.block_z:
            obs["observation"][2] = xinit[2] + self.z_offset
            obs["observation"][5] = xinit[2] + self.z_offset

        obs["dt"] = self.dt
        obs["pos_dif"] = self.pos_dif
        obs["center_x"] = self.center_x

        return obs


if __name__ == "__main__":
    register_custom_envs()
    # Call play.py in order to see current policy progress
    args = get_args()
    player = Player(args)
    player.initialize()
    player.play()
    # player.record_video(raw_path="/home/ssc/bachelor-thesis/videos/rollouts_{}_{}".format(args.env, args.play_policy))
