import random
import string

n=10000 
print("1")
print(n)

def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))
    
for i in range(n):
    t = random.randint(0, 110)
    resString = get_random_string(random.randint(1, 14)) +" "+get_random_string(random.randint(1, 14))+" "+str(t)
    listString = "".join(" "+get_random_string(1) for _ in range(t))
    print(resString+listString)
    
    
