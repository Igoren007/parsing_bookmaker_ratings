import requests

TOKEN = '1799874715:AAE0Rj4-SpV-OMAxLZg3hhbKIIueYwXZ9oM'
channel = -1001337710941

requests.get('https://api.telegram.org/bot{}/sendMessage'.format(TOKEN), params=dict(
   chat_id=channel,
   text='Hello world! from python'
))