# generate sample random sample python
import random
import string
import os

test = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
print(test)
os.system('cat test.txt')
