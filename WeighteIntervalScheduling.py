import random 
import sys
from functools import lru_cache

sys.setrecursionlimit(10**5)


N=int(sys.argv[1])
weights = list(random.randint(0,N) for _ in range(0,N,1))

@lru_cache(maxsize=10**5)
def opt_naive(i:int) -> int:
    if i ==0: return 0
    if i==1: return weights[0]
    drop = opt_naive(i-1)
    take = weights[i-1] + opt_naive(i-2)  #assume i is compatible with i-2
    res =  max(drop, take)
    return res


def opt_nonrec(weights):
    N= len(weights)
    OPT = [-1]*(N+1)    #-1,-1,-1,...,-1
    for i in range(N+1):  #i=0,1,2,3,4,...,n-1
        if i==0:
            res=0;
        elif i==1:
            res = weights[0]
        else:
            drop = OPT[i-1]
            take = weights[i-1] + OPT[i-2]
            res = max(drop, take)
        OPT[i] = res
    return OPT[N]



    
print(weights)
print(opt_naive(N))
print(opt_nonrec(weights))