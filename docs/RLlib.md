* RLlib(ray,tune) maybe the best RL library, it contains almost everything you need in RL domain, and it has the best performance. But it has some shortcomings, the biggest one is that it is very difficult to use. If you want to master it well, you maybe should read its source codes as much as possible.
* And few blogs and articles introduce the RLlib except the official website in the Internet, so I record the only articles about rllib.

---

## Blogs
* [Intro to RLlib: Example Environments](https://medium.com/distributed-computing-with-ray/intro-to-rllib-example-environments-3a113f532c70)
* [Anatomy of a custom environment for RLlib](https://medium.com/distributed-computing-with-ray/anatomy-of-a-custom-environment-for-rllib-327157f269e5)


## Source codes
* [anyscale/academy](https://github.com/anyscale/academy)

## Ask and answer
* [What does the ‘training_iteration’ parameter relate to in the RLlib?](https://discuss.ray.io/t/what-does-the-training-iteration-parameter-relate-to-in-the-rllib/2020)
>Each “training iteration” corresponds to one call to Trainer.train().

>A timestep is a single action taken in the environment.

>“Train episodes” is the number of episodes completed to create the batch used for training. Note that for batch_mode=“truncate_episodes”, there may be incomplete episodes (that don’t have done=True at the end) inside that train batch.

* [How to get mode summary if I use tune.run()?](https://discuss.ray.io/t/how-to-get-mode-summary-if-i-use-tune-run/2024)
> unfortunately, there is no way of getting the Trainer object directly from the tune.run() results. But you could do the following after tune.run:
```python
results = tune.run("PPO", config=[some config], checkpoint_at_end=True)
checkpoint = results.get_last_checkpoint()

# Create a new Trainer.
trainer = PPOTrainer(config=[same config as above])
trainer.restore(checkpoint)
trainer.get_policy().model.base_model.summary()
```

* [Why the episode reward mean is always the same number for a while(about 10 iters)?](https://discuss.ray.io/t/why-the-episode-reward-mean-is-always-the-same-number-for-a-while-about-10-iters/2009)
>Maybe your agent hasn’t learnt to reach the goal (+1) yet? This is a typical behavior for grid worlds where with per-step=-0.1 reward and some positive goal reward (along with episode termination).
Sounds completely normal.
Btw, the reported value under episode_reward_mean is the average reward from the train_batch used in that iteration.

* [[Tune] What parameters determine whether a trial RUNNING or PENDING? ](https://discuss.ray.io/t/tune-what-parameters-determine-whether-a-trial-running-or-pending/2032?u=bug404)
* >Hey @bug404, your machine/cluster has a set of resources available (e.g. 8 CPUs). Depending on your configuration, each trial might need 4 CPUs to run. In that case, two trials can be run at the same time and are thus in RUNNING state. The other trials are scheduled to run, but not running yet (because they are waiting for resources to become free), so they are in PENDING state.
