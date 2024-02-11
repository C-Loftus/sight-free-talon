# generate sample random sample python
import os
import random
import string

test = "".join(random.choice(string.ascii_lowercase) for i in range(10))
print(test)
os.system("cat test.txt")
