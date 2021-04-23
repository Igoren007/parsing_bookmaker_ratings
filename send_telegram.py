from requests import get

def write_message(TOKEN, channel_id, data):

    get('https://api.telegram.org/bot{}/sendMessage'.format(TOKEN), params=dict(
        chat_id=channel_id,
        text=data
    ))
