import numpy as np
import time

def selection_sort(alist,list_size):
    for i in range(list_size-1):
        tmp_min=i
        for j in range(i+1,list_size):
            if alist[j]<alist[tmp_min]:
                tmp_min=j
        
        alist[i],alist[tmp_min]=alist[tmp_min],alist[i]

  
if __name__=='__main__':
    alist=np.random.randint(0,10,size=10)
    print('before sort: ',alist)
    list_length=len(alist)
    selection_sort(alist, list_length)
    print('after sort: ',alist)
    
    blist=np.random.randint(0,10000,size=10000)
    list_length=len(blist)
    start_time=time.time()
    selection_sort(blist, list_length)
    print('elapsed time= ',time.time()-start_time)
    
# before sort:  [2 8 8 8 1 4 0 4 0 3]
# after sort:  [0 0 1 2 3 4 4 8 8 8]
# elapsed time=  9.69593620300293