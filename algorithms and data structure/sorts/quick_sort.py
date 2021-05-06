import numpy as np
import time
from copy import deepcopy

def quick_sort(alist):
    if len(alist)<=1:
        return
    k=alist[0]
    i,j=0,len(alist)-1
    while i!=j:
        while j>i and alist[j]>=k:
            j-=1
        alist[i],alist[j]=alist[j],alist[i]

        while i<j and alist[i]<=k:
            i+=1
        alist[i],alist[j]=alist[j],alist[i]
        
    quick_sort(alist[:i])
    quick_sort(alist[i+1:])

if __name__ == '__main__':
    alist = np.random.randint(0, 10, size=10)
    print('before sort: ', alist)
    list_length = len(alist)
    quick_sort(alist)
    print('after sort: ', alist)

    blist=np.random.randint(0,10000,size=10000)
    list_length=len(blist)
    start_time=time.time()
    quick_sort(blist)
    print('elapsed time= ',time.time()-start_time)

# before sort:  [8 0 7 2 6 4 1 2 0 2]
# after sort:  [0 0 1 2 2 2 4 6 7 8]
# elapsed time=  0.08011627197265625