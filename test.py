# from datetime import datetime
# import random
#
# day = str(datetime.now().day)
# s = '14:00 МСК/15 май'
#
# a = s.split('/')[1].split(' ')[0]
# print(type(a), type(day))
#
# print(random.randint(0,10))


import schedule
import time

def job():
    print("I'm working...")

schedule.every(1).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
# schedule.every().minute.at(":17").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)