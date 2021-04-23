import time
import requests
from bs4 import BeautifulSoup
import dbConnect
import pymongo
import send_telegram
from datetime import datetime



TOKEN = '1799874715:AAE0Rj4-SpV-OMAxLZg3hhbKIIueYwXZ9oM'
CHANNEL = -1001337710941
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'accept': '*/*'}

def save2db(collection, data):

    dbConnect.insert_document(collection, data)

def select_from_db(collection, query):

    return dbConnect.find_document(collection, query)

# this function returns HTML page code
def get_html(url, params=None):

    try:
        response = requests.get(url, headers=HEADERS, params=params).text
    except:
        response = ''
    return response


# this function returns a list of links to matches from this html page
def get_match_list(html):

    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='block-item iscroll-item has-image')
    links = []
    for item in items:
        link = item.a.get('href')
        links.append(link)
    return links


# gets the required data from the page
def get_bet_data(html, link):

    soup = BeautifulSoup(html, 'html.parser')
    match = soup.find('div', class_='match-block')
    kindOfSport = soup.find('ul', class_='breadcrumbs').find_all('li')[2].text.split(' ')[-1]
    bet_data = {
        "kindOfSport": kindOfSport,
        "link": link,
        "date": match.find('div', class_='date').text.strip(),
        "title": match.find('div', class_='name').text.strip(),
        "bet": match.find('div', class_='bet-name').text.strip(),
        "kf": match.a.get('data-factor-dec')
    }
    print(bet_data)
    return bet_data


def parser():

    bets = []
    for i in range(4):
        url = 'https://bookmaker-ratings.com.ua/ru/tips/tomorrow/?paged={}'.format(str(i+1))
        match_list = get_match_list(get_html(url))
        print(url)
        print(match_list)
        for item in match_list:
            print('---------------------------------------------------------------------')
            bets.append(get_bet_data(get_html(item), item))
    return bets


if __name__ == '__main__':

    time1 = time.time()
    bets = parser()
    collection_name = datetime.now().strftime("%d-%m-%Y")
    try:
        client = pymongo.MongoClient('localhost', 27017)
        db = client['pydbtest']
        col = db[collection_name]
    except:
        print('Connection to database error.')

    save2db(col, bets)

    sms = """
        Ставка по линии:

        """
    inf = select_from_db(col, {'kindOfSport': 'футбол'})
    sms += inf['title'] + ': ' + inf['bet']

    print(sms)
    send_telegram.write_message(TOKEN, CHANNEL, sms)
    time2 = time.time()
    print('Work time: {}'.format(time2 - time1))

