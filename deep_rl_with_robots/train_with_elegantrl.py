from elegantrl.agent import AgentPPO
import gym
from elegantrl.env import PreprocessEnv
from elegantrl.run import Arguments,train_and_evaluate,train_and_evaluate_mp

if __name__=='__main__':
    args=Arguments(if_on_policy=True)
    args.agent=AgentPPO()
    args.agent.if_use_gae=True
    args.agent.lambda_entropy=0.04

    from kuka_cam_reach_env import KukaCamReachEnv,CustomSkipFrame

    env_config = {
        "is_render": False,
        "is_good_view": False,
        "max_steps_one_episode": 1000,
    }

    args.env=CustomSkipFrame(KukaCamReachEnv(config=env_config))
    args.gamma=0.995
    args.break_step = int(3e5)
    args.net_dim = 2 ** 9
    args.max_step = args.env.max_step
    args.max_memo = args.max_step * 4
    args.batch_size = 2 ** 10
    args.repeat_times = 2 ** 3
    args.eval_gap = 2 ** 4
    args.eval_times1 = 2 ** 3
    args.eval_times2 = 2 ** 5
    args.if_allow_break = False

    '''train and evaluate'''
    # train_and_evaluate(args)
    args.rollout_num = 1
    train_and_evaluate(args)
