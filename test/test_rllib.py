import argparse
import os

import ray
import ray.tune as tune
from ray.tune import sample_from
from ray.rllib.examples.env.fast_image_env import FastImageEnv
from ray.rllib.examples.models.fast_model import FastModel, TorchFastModel
from ray.rllib.models import ModelCatalog
from ray.rllib.models.modelv2 import ModelV2
from ray.rllib.models.torch.misc import SlimFC
from ray.rllib.models.torch.torch_modelv2 import TorchModelV2
from ray.rllib.utils.annotations import override
from ray.rllib.utils.framework import try_import_torch
import torch.nn.functional as F

torch,nn=try_import_torch()

# env=FastImageEnv(config={})
# print(env)
# print(env.observation_space)

# a=env.action_space.sample()
# print(a)
# o,r,d,info=env.step(a)
# print(o,r,d,info)

class TorchFastModel(TorchModelV2,nn.Module):


    def __init__(self, obs_space, action_space, num_outputs, model_config,
                 name):
        
        TorchModelV2.__init__(self, obs_space, action_space, num_outputs,
                              model_config, name)
        nn.Module.__init__(self)
        
        self.conv1 = nn.Conv2d(obs_space, 32, 3, stride=2, padding=1)
        self.conv2 = nn.Conv2d(32, 32, 3, stride=2, padding=1)
        self.conv3 = nn.Conv2d(32, 32, 3, stride=2, padding=1)
        self.conv4 = nn.Conv2d(32, 32, 3, stride=2, padding=1)

        # The output image size is calculated through
        # (I - K + 2*P) / S + 1
        # where: I : image size, the initial image size is 84x84, so I == 84 here.
        #        K : kernel size, here is 3
        #        P : padding size, here is 1
        #        S : stride, here is 2
        # So 84x84 image will become 6x6 through the ConvNet above. And 32 is the filters number.
        self.fc1 = nn.Linear(32 * 6 * 6, 512)
        self.fc_out = nn.Linear(512, num_outputs)
        self._initialize_weights()

    def _initialize_weights(self):
        for module in self.modules():
            if isinstance(module, nn.Conv2d) or isinstance(module, nn.Linear):
                nn.init.xavier_uniform_(module.weight)
                # nn.init.kaiming_uniform_(module.weight)
                nn.init.constant_(module.bias, 0)
            elif isinstance(module, nn.LSTMCell):
                nn.init.constant_(module.bias_ih, 0)
                nn.init.constant_(module.bias_hh, 0)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = F.relu(self.conv4(x))
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        out = self.fc_out(x)
        return out.squeeze()
    
if __name__=='__main__':

    ray.shutdown()
    ray.init()
    ModelCatalog.register_custom_model("fast_model",TorchFastModel)
    
    config={
        "env":FastImageEnv,
        "model":{
            "custom_model":"fast_model"
        },
        
        "num_gpus":1,
        "num_workers":1,
        "framework":"torch",
    }
    
    tune.run("PPO",config=config,verbose=1)
    
    ray.shutdown()