import numpy as np
import time

def insertion_sort(alist,list_length):
    for i in range(1,list_length):
        for j in range(0,i):
            if alist[j]>alist[i]:
                tmp=alist[i]
                for k in range(i,j,-1):
                    alist[k]=alist[k-1]
                alist[j]=tmp
                break
            
  
if __name__=='__main__':
    alist=np.random.randint(0,10,size=10)
    print('before sort: ',alist)
    list_length=len(alist)
    insertion_sort(alist, list_length)
    print('after sort: ',alist)
    
    blist=np.random.randint(0,10000,size=10000)
    list_length=len(blist)
    start_time=time.time()
    insertion_sort(blist, list_length)
    print('elapsed time= ',time.time()-start_time)
    
# before sort:  [7 8 8 1 9 9 9 2 6 1]
# after sort:  [1 1 2 6 7 8 8 9 9 9]
# elapsed time=  8.602885723114014