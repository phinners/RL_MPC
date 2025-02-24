import time

import tensorflow as tf

from common import get_args
from env_ext import make_env
from envs import register_custom_envs
from policies import Policy, make_policy


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Tester:
    policy: Policy = None

    def __init__(self, args):
        # initialize environment
        self.args = args
        self.env = make_env(args)
        # self.args.timesteps = self.env.env.env.spec.max_episode_steps
        self.info = []
        self.test_rollouts = args.episodes
        self.mode = args.play_mode
        self.policy = make_policy(args)
        self.policy.set_envs(envs=[self.env])

        # setup logger
        args.logger.summary_init(None, None)
        args.logger.add_item('Episode')
        args.logger.add_item('TimeCost(sec)')
        args.logger.add_item('Timesteps')
        args.logger.add_item('Collisions')
        args.logger.add_item('ExReward')
        args.logger.add_item('Success')
        args.logger.add_item('Success/mpc')
        args.logger.add_item('Seed')
        args.logger.add_item('Computational Time')

    def test(self):
        env = self.env
        test_col_tolerance = self.args.test_col_tolerance
        acc_sum = 0.0
        col_sum = 0.0
        step_sum = 0.0
        succ_step_sum = 0.0
        tol_acc_sum = 0.0
        start_seed = 1000
        comp_time = 0.0
        comp_sum = 0.0

        for i in range(self.test_rollouts):
            env.np_random.seed(start_seed + i)
            self.policy.reset()
            ob = env.reset()
            env_info = None
            logger_timesteps = 0

            args.logger.tabular_clear()
            args.logger.summary_clear()

            if args.play_policy in ['MPCPolicy']:
                self.policy.set_sub_goals([ob['desired_goal']])

            for timestep in range(args.timesteps):
                start_time = time.time()
                actions, infos = self.policy.predict(obs=[ob])
                comp_time = time.time() - start_time
                comp_sum += comp_time
                action = actions[0]
                ob, reward, _, env_info = env.step(action)
                logger_timesteps += 1

                # env.render()

                if env_info['Success']:
                    break

            args.logger.add_record('Episode', i)
            args.logger.add_record('Success', int(env_info['Success']))
            args.logger.add_record('TimeCost(sec)', env.time)
            args.logger.add_record('Timesteps', logger_timesteps)
            args.logger.add_record('Collisions', env.collisions)
            args.logger.add_record('ExReward', env_info['ExReward'])
            args.logger.add_record('Success/mpc', int(env.collisions <= test_col_tolerance and env_info['Success']))
            args.logger.add_record('Seed', start_seed + i)
            args.logger.add_record('Computational Time', comp_time)

            acc_sum += env_info['Success']
            col_sum += env.collisions
            step_sum += logger_timesteps
            if env_info['Success']:
                succ_step_sum += logger_timesteps
            if env.collisions <= test_col_tolerance:
                tol_acc_sum += env_info['Success']

            args.logger.tabular_show()
            args.logger.save_csv(filename="test_policy_{}_tol{}_run{}"
                                 .format(args.play_policy, test_col_tolerance, args.test_run_id))

        tol_acc = tol_acc_sum / self.test_rollouts

        print('Success rate: {}'.format(acc_sum / self.test_rollouts))
        print(bcolors.WARNING + 'Success rate (tol): {}'.format(tol_acc) + bcolors.ENDC)
        print('Mean Timesteps per Episode: {}'.format(step_sum / self.test_rollouts))
        print('Mean Timesteps per Succesfull Episode: {}'.format(succ_step_sum / acc_sum))
        print('Mean Collisions per Episode: {}'.format(col_sum / self.test_rollouts))
        print('Collisions sum: ', col_sum)
        print('Mean Computational Time [s] per Timestep: {}'.format(comp_sum / step_sum))


if __name__ == "__main__":
    tf.compat.v1.disable_eager_execution()
    register_custom_envs()

    args = get_args()
    tester = Tester(args)
    tester.test()
