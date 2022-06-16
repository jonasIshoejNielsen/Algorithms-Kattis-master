import random
import string
"""
c=2000 
n=2000 


for case in range(1,31):
    print(str(c)+" "+str(n))

    for i in range(n):
        v = random.randint(1, 10000)
        w = random.randint(1, 10000)
        print(str(v)+" "+str(w))
"""
n = 1000
print(n)
for _ in range(n):
    res = ""
    for _ in range(n):
        res += "."
    print(res)