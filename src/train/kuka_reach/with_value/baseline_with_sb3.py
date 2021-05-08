import gym
import numpy as np

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.utils import set_random_seed
from custom_env import KukaReachEnv
from stable_baselines3.common.evaluation import evaluate_policy
env_config = {
    "is_render": False,
    "is_good_view": False,
    "max_steps_one_episode": 1000,
    "seed":4
}


def make_env(rank, seed=0):
    """
    Utility function for multiprocessed env.

    :param env_id: (str) the environment ID
    :param num_env: (int) the number of environments you wish to have in subprocesses
    :param seed: (int) the inital seed for RNG
    :param rank: (int) index of the subprocess
    """
    def _init():
        env = KukaReachEnv(env_config)
        env.seed(seed + rank)
        return env
    set_random_seed(seed)
    return _init

if __name__ == '__main__':
    
    num_cpu = 6  # Number of processes to use
    # Create the vectorized environment
    env = SubprocVecEnv([make_env(i) for i in range(num_cpu)])
    env_for_evaluate=KukaReachEnv(env_config)
    # Stable Baselines provides you with make_vec_env() helper
    # which does exactly the previous steps for you:
    # env = make_vec_env(env_id, n_envs=num_cpu, seed=0)

    model = PPO('MlpPolicy', env, verbose=1)
    model.learn(total_timesteps=10000000)
    mean_reward, std_reward = evaluate_policy(model, env_for_evaluate, n_eval_episodes=1)
    print(f"mean_reward:{mean_reward:.2f} +/- {std_reward:.2f}")
    # obs = env.reset()
    # for _ in range(1000):
    #     action, _states = model.predict(obs)
    #     obs, rewards, dones, info = env.step(action)
    #     env.render()