# Deep learning in RL

* 强化学习中的CNN一般没有池化层，池化层会让你获得平移不变性，即网络对图像中对象的位置变得不敏感。这对于 ImageNet 这样的分类任务来说是有意义的，但游戏中位置对潜在的奖励至关重要，我们不希望丢失这些信息。
* 经验回放的动机是：①深度神经网络作为有监督学习模型，要求数据满足独立同分布；②通过强化学习采集的数据之间存在着关联性，利用这些数据进行顺序训练，神经网络表现不稳定，而经验回放可以打破数据间的关联。
* [深度学习——Xavier初始化方法](https://blog.csdn.net/shuzfan/article/details/51338178)
* [深入解读xavier初始化（附源码）](https://zhuanlan.zhihu.com/p/43840797)
* [PyTorch 学习笔记（四）：权值初始化的十种方法](https://zhuanlan.zhihu.com/p/53712833)

