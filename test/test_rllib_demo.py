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
   
    ray.init()

    ModelCatalog.register_custom_model(
        "fast_model", TorchFastModel)

    config = {
        "env": FastImageEnv,
       
        "model": {
            "custom_model": "fast_model"
        },
        # Use GPUs iff `RLLIB_NUM_GPUS` env var set to > 0.
        "num_gpus": 1,
        "num_workers": 1,
        "framework": "torch",
    }
    

    config_for_trainer = {
       
        "model": {
            "custom_model": "fast_model"
        },
        # Use GPUs iff `RLLIB_NUM_GPUS` env var set to > 0.
        "num_gpus": 1,
        "num_workers": 1,
        "framework": "torch",
    }

    
    tune.run("PPO", config=config, verbose=1)

    ray.shutdown()
