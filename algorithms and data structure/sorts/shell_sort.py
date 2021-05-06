import numpy as np
import time

# This implementation is a copy version of the Java implementation in the Algorithm (4th edition)
# But its performance is very bad. 

# * before sort:  [7 6 6 4 9 8 4 2 0 1]
# * after sort:  [0 1 2 4 4 6 6 7 8 9]
# * elapsed time=  14.546229839324951

def shell_sort_from_java(alist):
    length=len(alist)
    h=1
    while h<length//3:
        h=3*h+1
    while h>=1:
        for i in range(h,length):
            for j in range(i,h-1,-h):
                if alist[j]<alist[j-h]:
                    alist[j],alist[j-h]=alist[j-h],alist[j]
        h=h//3

# before sort:  [0 5 3 6 2 9 4 5 6 7]
# after sort:  [0 2 3 4 5 5 6 6 7 9]
# elapsed time=  0.07308650016784668
def shell_sort(arr):
  
    # Start with a big gap, then reduce the gap
    n = len(arr)
    gap = n//2
  
    # Do a gapped insertion sort for this gap size.
    # The first gap elements a[0..gap-1] are already in gapped 
    # order keep adding one more element until the entire array
    # is gap sorted
    while gap > 0:
  
        for i in range(gap,n):
  
            # add a[i] to the elements that have been gap sorted
            # save a[i] in temp and make a hole at position i
            temp = arr[i]
  
            # shift earlier gap-sorted elements up until the correct
            # location for a[i] is found
            j = i
            while  j >= gap and arr[j-gap] >temp:
                arr[j] = arr[j-gap]
                j -= gap
  
            # put temp (the original a[i]) in its correct location
            arr[j] = temp
        gap =gap//2

if __name__ == '__main__':
    alist = np.random.randint(0, 10, size=10)
    print('before sort: ', alist)
    list_length = len(alist)
    shell_sort(alist)
    print('after sort: ', alist)

    blist=np.random.randint(0,10000,size=10000)
    list_length=len(blist)
    start_time=time.time()
    shell_sort(blist)
    print('elapsed time= ',time.time()-start_time)

