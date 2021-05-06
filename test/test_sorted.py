from typing import List
nums = [3,30,34,5,9]
# alist=list(map(str,nums))
# print(alist)

# def Compare(str):
#     def __lt__(x,y):
#         return x+y<y+x
    
# ans=sorted(map(str,nums),key=Compare,reverse=True)
# print(ans)
alist=['2','1','3','0']
class Compare(str):
    def __lt__(x, y):
        print('x=',x,'y=',y)
        print(x+y<y+x)
        print()
        return x+y<y+x
ans=sorted(alist,key=Compare)   
# class Solution:
#     def largestNumber(self, nums: List[int]) -> str:
#         largest_num = ''.join(sorted(map(str, nums), key=Compare, reverse=True))
#         return '0' if largest_num[0] == '0' else largest_num
    
# sol=Solution()
# ans=sol.largestNumber(nums)
print(ans)