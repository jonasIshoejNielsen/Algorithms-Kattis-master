import random 
import sys
import math
from functools import lru_cache

sys.setrecursionlimit(10**5)

a=int(sys.argv[1])
n=int(sys.argv[2])

@lru_cache(maxsize=10**5)
def opt(i:int) -> int:
    if i ==0: return 1
    if i==1: return a
    resPrev1 = opt(math.floor(i/2))
    resPrev2 = opt(math.ceil(i/2))
    res =  resPrev1*resPrev2
    return res


print(opt(n))
print(a**n)