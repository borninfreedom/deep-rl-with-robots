#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   baseline_with_erl.py
@Time    :   2021/04/30 16:36:59
@Author  :   Yan Wen 
@Version :   1.0
@Contact :   z19040042@s.upc.edu.cn
@Desc    :   None
'''

# here put the import lib

from elegantrl.run import *
from elegantrl.agent import AgentPPO

from custom_env import KukaReachEnv

config={
    'is_render':False,
    'is_good_view':False,
    'max_steps_one_episode':1000
}

args=Arguments(if_on_policy=True)
args.agent=AgentPPO()
args.env=KukaReachEnv(config)
args.gamma=0.95
args.rollout_num=3

train_and_evaluate_mp(args)
