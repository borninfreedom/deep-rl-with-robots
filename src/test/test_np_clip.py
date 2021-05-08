alist = [1, 2, 3, 4]
blist = alist[1:3]
alist[1:3] = [5, 5]
print('blist: ', blist)

import numpy as np

alist = np.array([1, 2, 3, 4])
blist = alist[1:3]
alist[1:3] = [5, 5]
print('blist: ', blist)


# ! This program is very interesting, the explanation is here. 
# ! [numpy的切片和python的切片区别](https://blog.csdn.net/bornfree5511/article/details/116375695)