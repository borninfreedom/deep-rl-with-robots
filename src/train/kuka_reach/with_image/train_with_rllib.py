import time
import ray
import ray.rllib.agents.ppo as ppo
from ray.tune.logger import pretty_print
from env import CustomSkipFrame, KukaCamReachEnv
from ray import tune
from ray.tune import grid_search
from ray.rllib.env.env_context import EnvContext
from ray.tune.registry import register_env, register_trainable
from ray.rllib.agents.ppo import PPOTrainer
from ray.rllib.agents.impala import ImpalaTrainer

if __name__=='__main__':
        
    ray.shutdown()
    ray.init(ignore_reinit_error=True)

    # env_config={
    #     "is_render":False,
    #     "is_good_view":False,
    #     "max_steps_one_episode":1000,
    # }
    # env=KukaCamReachEnv(env_config)
    # env=CustomSkipFrame(env)
    
    register_env("kuka_env",lambda config: CustomSkipFrame(KukaCamReachEnv(config)))
    #register_env("kuka_env",lambda config: KukaCamReachEnv(config))
    
    
    config = {
        "env": "kuka_env",
        "model":{
            "conv_filters":[[32,[3,3],2],[32,[3,3],2],[32,[3,3],2],[32,[3,3],2],[1152,[6,6],1]],
           # "conv_filters":"relu",
            "post_fcnet_hiddens":[512,251],
            "post_fcnet_activation":"relu",
        },
        "env_config":{
            "is_render":False,
            "is_good_view":False,
            "max_steps_one_episode":1000,
        },
        "num_workers":10,
        "num_gpus":1,
        "framework":"torch",
        # "render_env":False,
        # "num_gpus_per_worker":0,
      #  "num_envs_per_worker":5,
        # "rollout_fragment_length":1000,
        # "train_batch_size":4000,
       # "batch_mode":"complete_episodes",
        #"lr":0.0001,
       # "lr":grid_search([5e-5,0.0001])
    }

    config_for_trainer = {
        "env": "kuka_env",
        # "model":{
        #     "conv_filters":[[32,[3,3],2],[32,[3,3],2],[32,[3,3],2],[32,[3,3],2],[1152,[6,6],1]],
        #    # "conv_filters":"relu",
        #     "post_fcnet_hiddens":[512,251],
        #     "post_fcnet_activation":"relu",
        # },
        "env_config":{
            "is_render":False,
            "is_good_view":False,
            "max_steps_one_episode":1000,
        },
        "num_workers":1,
        "num_gpus":1,
        "framework":"torch",
    }

    stop = {
        "episode_reward_mean": 0.99,
        "training_iteration":200,
    }

    # trainer=PPOTrainer(config=config_for_trainer)
    # print(trainer.get_policy().model)
    #
    # trainer=ImpalaTrainer(config=config_for_trainer)
    # print(trainer.get_policy().model)
    
    
    results = tune.run(
        "SAC", # Specify the algorithm to train
        config=config,
        stop=stop,
        checkpoint_freq=1,
    )

    metric="episode_reward_mean"
    best_trial = results.get_best_trial(metric=metric, mode="max", scope="all")
    best_checkpoint=results.get_best_checkpoint(best_trial,metric=metric,mode="max")
    print('best checkpoint: ',best_checkpoint)
   
    ray.shutdown()