import numpy as np
import time
from copy import deepcopy

def merge_sort(alist):
    if len(alist) > 1:
        mid = len(alist) // 2
        left_half = deepcopy(alist[:mid])
        right_half = deepcopy(alist[mid:])

        merge_sort(left_half)
        merge_sort(right_half)

        _merge(alist, left_half, right_half)


def _merge(alist, left_half, right_half):
    i, j, k = 0, 0, 0
    #print('merge alist: ', alist)
    while i < len(left_half) and j < len(right_half):
        if left_half[i] < right_half[j]:
            alist[k] = left_half[i]
            i += 1

        else:
            alist[k] = right_half[j]
            j += 1

        k += 1

    while i < len(left_half):
        alist[k] = left_half[i]
        i += 1
        k += 1

    while j < len(right_half):
        alist[k] = right_half[j]
        j += 1
        k += 1


if __name__ == '__main__':
    alist = np.random.randint(0, 10, size=10)
    print('before sort: ', alist)
    list_length = len(alist)
    merge_sort(alist)
    print('after sort: ', alist)

    blist=np.random.randint(0,10000,size=10000)
    list_length=len(blist)
    start_time=time.time()
    merge_sort(blist)
    print('elapsed time= ',time.time()-start_time)

# before sort:  [9 1 7 1 6 6 4 0 6 8]
# after sort:  [0 1 1 4 6 6 6 7 8 9]
# elapsed time=  0.08119559288024902