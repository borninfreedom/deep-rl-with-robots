"""Example of using a custom image env and model.

Both the model and env are trivial (and super-fast), so they are useful
for running perf microbenchmarks.
"""

import argparse
import os

import ray
import ray.tune as tune
from ray.tune import sample_from
from fast_image_env import FastImageEnv
from fast_model import TorchFastModel,TorchCustomFastModel
from ray.rllib.models import ModelCatalog
from ray.rllib.agents.ppo import PPOTrainer

if __name__ == "__main__":
   
    ray.shutdown()
    ray.init()

    config = {
        "env": FastImageEnv,
        # Use GPUs iff `RLLIB_NUM_GPUS` env var set to > 0.
        "num_gpus": 0,
        "num_workers": 1,
        "framework": "torch",
    }
    
    trainer=PPOTrainer(config=config)
    print(trainer.get_policy().model)
    
    results=tune.run("PPO",config=config,verbose=3)
    print(results)
    
    ray.shutdown()
