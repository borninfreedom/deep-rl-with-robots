from ray.rllib.models.modelv2 import ModelV2

from ray.rllib.models.torch.misc import SlimFC, SlimConv2d
from ray.rllib.models.torch.torch_modelv2 import TorchModelV2
from ray.rllib.utils.annotations import override
from ray.rllib.utils.framework import try_import_torch

torch, nn = try_import_torch()

# class TorchCustomFastModel(TorchModelV2,nn.Module):
#     def __init__(self, obs_space, action_space, num_outputs, model_config,
#                 name):
#         TorchModelV2.__init__(self, obs_space, action_space, num_outputs,
#                               model_config, name)
#         nn.Module.__init__(self)
        
#         self.conv1=SlimConv2d(obs_space.shape[2],32,3,2,1)
#         self.conv2=SlimConv2d(32,32,3,2,1)
#         self.conv3=SlimConv2d(32,32,3,2,1)
#         self.conv4=SlimConv2d(32,32,3,2,1)
#         self.fc1=SlimFC(32*6*6,512)
#         self.fc_out=SlimFC(512,num_outputs)

#     @override(ModelV2)
#     def forward(self, input_dict, state, seq_lens):
#         x=self.conv1()
        

class TorchFastModel(TorchModelV2, nn.Module):
    """Torch version of FastModel (tf)."""

    def __init__(self, obs_space, action_space, num_outputs, model_config,
                 name):
        TorchModelV2.__init__(self, obs_space, action_space, num_outputs,
                              model_config, name)
        nn.Module.__init__(self)

        print('obs space: ', obs_space)
        print('action_space: ',action_space)
        print('num outpus: ',num_outputs)
        print('model config: ',model_config)
        print('name: ',name)
        
        self.bias = nn.Parameter(
            torch.tensor([0.0], dtype=torch.float32, requires_grad=True))

        # Only needed to give some params to the optimizer (even though,
        # they are never used anywhere).
        self.dummy_layer = SlimFC(1, 1)
        self._output = None

    @override(ModelV2)
    def forward(self, input_dict, state, seq_lens):
        print('input dict: ',input_dict)
        #print('input dict obs: ',input_dict['obs'])
        print('input dict obs shape: ',input_dict['obs'].shape)
        print('state: ',state)
        print('seq lens: ',seq_lens)
        
        self._output = self.bias + torch.zeros(
            size=(input_dict["obs"].shape[0], self.num_outputs)).to(
                self.bias.device)
 
        return self._output, []
    
    @override(ModelV2)
    def value_function(self):
        assert self._output is not None, "must call forward first!"
        return torch.reshape(torch.mean(self._output, -1), [-1])




# class TorchFastModel(TorchModelV2, nn.Module):
#     """Torch version of FastModel (tf)."""

#     def __init__(self, obs_space, action_space, num_outputs, model_config,
#                  name):
#         TorchModelV2.__init__(self, obs_space, action_space, num_outputs,
#                               model_config, name)
#         nn.Module.__init__(self)

#         self.bias = nn.Parameter(
#             torch.tensor([0.0], dtype=torch.float32, requires_grad=True))

#         # Only needed to give some params to the optimizer (even though,
#         # they are never used anywhere).
#         self.dummy_layer = SlimFC(1, 1)
#         self._output = None

#     @override(ModelV2)
#     def forward(self, input_dict, state, seq_lens):
#         self._output = self.bias + torch.zeros(
#             size=(input_dict["obs"].shape[0], self.num_outputs)).to(
#                 self.bias.device)
 
#         return self._output, []
    
#     @override(ModelV2)
#     def value_function(self):
#         assert self._output is not None, "must call forward first!"
#         return torch.reshape(torch.mean(self._output, -1), [-1])
