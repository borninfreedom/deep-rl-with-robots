import time
import ray
import ray.rllib.agents.ppo as ppo
from ray.tune.logger import pretty_print
from env import KukaCamReachEnv
from ray import tune
from ray.tune import grid_search
from ray.rllib.env.env_context import EnvContext
from ray.tune.registry import register_trainable
from ray.rllib.agents.ppo import PPOTrainer

ray.shutdown()
ray.init(ignore_reinit_error=True)

config = {
    "env": KukaCamReachEnv,
    "env_config":{
        "is_render":False,
        "is_good_view":False,
        "max_steps_one_episode":1000,
        #"seed":10
    },
    "model":{
        "fcnet_hiddens":[64,64],
        "fcnet_activation":"tanh"
    },
    "num_workers":1,
    "num_gpus":1,
    "framework":"torch",
    "render_env":False,
    "num_gpus_per_worker":0,
    "num_envs_per_worker":1,
    "rollout_fragment_length":1000,
    "train_batch_size":4000,
    "batch_mode":"complete_episodes",
    "lr":grid_search([0.0001,5e-5,0.001,0.01])
}

stop = {
    "episode_reward_mean": 1,
    "training_iteration":500,
}

ModelPrintPPOTrainer = PPOTrainer.with_updates(after_init=lambda trainer: trainer.get_policy().model.base_model.summary())
register_trainable("ModelPrintPPOTrainer", ModelPrintPPOTrainer)
st=time.time()
results = tune.run(
    "ModelPrintPPOTrainer", # Specify the algorithm to train
    config=config,
    stop=stop,
    checkpoint_freq=1,
)
#tune.run("ModelPrintPPOTrainer",...)
# trainer=ppo.PPOTrainer(config=config)
# print(trainer.get_policy().model.base_model.summary())
# metric="episode_reward_mean"
# best_trial = results.get_best_trial(metric=metric, mode="max", scope="all")
# best_checkpoint=results.get_best_checkpoint(best_trial,metric=metric,mode="max")

# print('best checkpoint: ',best_checkpoint)
# print("elapsed time=",time.time()-st)
 
ray.shutdown()