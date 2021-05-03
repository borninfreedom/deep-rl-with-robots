import numpy as np
import time

def bubble_sort(alist,list_length):
    for i in range(list_length-1,0,-1):
        for j in range(i):
            if alist[j]>alist[j+1]:
                alist[j],alist[j+1]=alist[j+1],alist[j]
                
  
if __name__=='__main__':
    alist=np.random.randint(0,10,size=10)
    print('before sort: ',alist)
    list_length=len(alist)
    bubble_sort(alist, list_length)
    print('after sort: ',alist)
    
    blist=np.random.randint(0,10000,size=10000)
    list_length=len(blist)
    start_time=time.time()
    bubble_sort(blist, list_length)
    print('elapsed time= ',time.time()-start_time)
    
# before sort:  [7 8 8 1 9 9 9 2 6 1]
# after sort:  [1 1 2 6 7 8 8 9 9 9]
# elapsed time=  8.602885723114014