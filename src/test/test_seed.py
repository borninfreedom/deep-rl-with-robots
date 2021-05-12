from gym.utils import seeding

import random

np_random,seed=seeding.np_random(1)
random.seed(1)


print(np_random.uniform(-0.4,0.4))
print(random.uniform(-0.4,0.4))

