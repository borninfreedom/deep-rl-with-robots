from typing import List

from copy import deepcopy
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        import numpy as np
        n = len(prices)
        dp=np.zeros((n,3,2),dtype=np.int32)
        #dp=[[[0]*2]*3 for _ in range(n)]
        print(dp)
        # dp=np.array(dp)
        print(dp.shape)

        dp[0][1][1]=-prices[0]
        dp[0][1][0]=0
        dp[0][2][0]=0
        dp[0][2][1]=-prices[0]
        # dp_0_0 = 0
        # dp_1_0 = 0
        # dp_1_1 = -prices[0]
        # dp_2_0 = 0
        # dp_2_1 = -prices[0]
        for i in range(1, n):
            # dp_2_0 = max(dp_2_0, dp_2_1 + prices[i])
            # dp_2_1 = max(dp_2_1, dp_1_0 - prices[i])
            # dp_1_0 = max(dp_1_0, dp_1_1 + prices[i])
            # dp_1_1 = max(dp_1_1, dp_0_0 - prices[i])
            dp[i][2][0]=max(deepcopy(dp[i-1][2][0]),deepcopy(dp[i-1][2][1])+prices[i])
            dp[i][2][1]=max(deepcopy(dp[i-1][2][1]),deepcopy(dp[i-1][1][0])-prices[i])
            dp[i][1][0]=max(deepcopy(dp[i-1][1][0]),deepcopy(dp[i-1][1][1])+prices[i])
            dp[i][1][1]=max(deepcopy(dp[i-1][1][1]),deepcopy(dp[i-1][0][0])-prices[i])

        return dp[-1][2][0]

sol=Solution()
print(sol.maxProfit([3,3,5,0,0,3,1,4]))
