"""Example of using a custom image env and model.

Both the model and env are trivial (and super-fast), so they are useful
for running perf microbenchmarks.
"""

import argparse
import os

import ray
import ray.tune as tune
from ray.tune import sample_from
from ray.rllib.examples.env.fast_image_env import FastImageEnv
from fast_model import TorchFastModel
from ray.rllib.models import ModelCatalog
from ray.rllib.agents.ppo import PPOTrainer

if __name__ == "__main__":
   
    env=FastImageEnv({})
    print(env.observation_space.shape)
    print(env.action_space)