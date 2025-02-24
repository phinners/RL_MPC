import gym

from .franka.franka_pick_dyn_lifted_obstacles import FrankaPickDynLiftedObstaclesEnv
from .franka.franka_pick_dyn_obstacles import FrankaPickDynObstaclesEnv
from .franka.franka_pick_dyn_obstacles2 import FrankaPickDynObstaclesEnv2
from .franka.franka_pick_dyn_sqr_obstacle import FrankaPickDynSqrObstacleEnv
from .franka.franka_pick_dyn_sqr_obstacles import FrankaPickDynSqrObstaclesEnv


def register_custom_envs():
    gym.envs.register(
        id='FrankaPickDynSqrObstacle-v1',
        entry_point='envs_real:FrankaPickDynSqrObstacleEnv',
        max_episode_steps=100,
        kwargs={'reward_type': 'sparse', 'n_substeps': 20},
    )
    gym.envs.register(
        id='FrankaPickDynSqrObstacles-v1',
        entry_point='envs_real:FrankaPickDynSqrObstaclesEnv',
        max_episode_steps=100,
        kwargs={'reward_type': 'sparse', 'n_substeps': 20},
    )
    gym.envs.register(
        id='FrankaFetchPickDynObstaclesEnv-v1',
        entry_point='envs_real:FrankaPickDynObstaclesEnv',
        max_episode_steps=100,
        kwargs={'reward_type': 'sparse', 'n_substeps': 20},
    )
    gym.envs.register(
        id='FrankaPickDynObstacles-v2',
        entry_point='envs_real:FrankaPickDynObstaclesEnv2',
        max_episode_steps=100,
        kwargs={'reward_type': 'sparse', 'n_substeps': 20},
    )
    gym.envs.register(
        id='FrankaPickDynLiftedObstacles-v1',
        entry_point='envs_real:FrankaPickDynLiftedObstaclesEnv',
        max_episode_steps=100,
        kwargs={'reward_type': 'sparse', 'n_substeps': 20},
    )
    gym.envs.register(
        id='FrankaFetchPickDynLiftedObstacles-v1',
        entry_point='envs_real:FrankaPickDynLiftedObstaclesEnv',
        max_episode_steps=100,
        kwargs={'reward_type': 'sparse', 'n_substeps': 20},
    )
    gym.envs.register(
        id='FrankaFetchPickDynLiftedObstaclesEnv-v1',
        entry_point='envs_real:FrankaPickDynLiftedObstaclesEnv',
        max_episode_steps=100,
        kwargs={'reward_type': 'sparse', 'n_substeps': 20},
    )
