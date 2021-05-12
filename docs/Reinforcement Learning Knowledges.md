![image-20210511121346365](C:\Users\yan\deep-rl-with-robots\docs\Reinforcement Learning Knowledges.assets\image-20210511121346365.png)

* 对于一个强化学习 Agent，它由什么组成？
```
答：

策略函数（policy function），Agent会用这个函数来选取它下一步的动作，包括随机性策略（stochastic policy）和确定性策略（deterministic policy）。

价值函数（value function），我们用价值函数来对当前状态进行评估，即进入现在的状态，到底可以对你后面的收益带来多大的影响。当这个价值函数大的时候，说明你进入这个状态越有利。

模型（model），其表示了 Agent 对这个Environment的状态进行的理解，它决定了这个系统是如何进行的。
```
