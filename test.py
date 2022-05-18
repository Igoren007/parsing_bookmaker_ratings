from datetime import datetime
import random

day = str(datetime.now().day)
s = '14:00 МСК/15 май'

a = s.split('/')[1].split(' ')[0]
print(type(a), type(day))

print(random.randint(0,10))