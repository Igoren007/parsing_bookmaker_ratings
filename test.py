from datetime import datetime

day = str(datetime.now().day)
s = '14:00 МСК/15 май'

a = s.split('/')[1].split(' ')[0]
print(type(a), type(day))