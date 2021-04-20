import time
import requests
from bs4 import BeautifulSoup
import sqlite3

URL = 'https://bookmaker-ratings.com.ua/ru/tips/today/'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'accept': '*/*'}

def save_to_db(bets):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO data VALUES (?,?,?,?)", bets)
    conn.commit()

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params).text
    return r


def get_match_list(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='block-item iscroll-item has-image')
    links = []
    for item in items:
        link = item.a.get('href')
        links.append(link)
    return links


def get_bet_data(html, link):
    soup = BeautifulSoup(html, 'html.parser')
    match = soup.find('div', class_='match-block')
    bet_info = (
        link,
        match.find('div', class_='date').text.strip(),
        match.find('div', class_='name').text.strip(),
        match.find('div', class_='bet-name').text.strip(),
    )
    print(bet_info)
    return bet_info


def parser():
    bets = []
    time1 = time.time()
    start_link = URL
    match_list = get_match_list(get_html(start_link))
    for item in match_list:
        print('******************************************************************')
        bets.append(get_bet_data(get_html(item), item))
    time2 = time.time()
    print(bets)
    save_to_db(bets)
    print('Work time: {}'.format(time2 - time1))


if __name__ == '__main__':
    parser()
