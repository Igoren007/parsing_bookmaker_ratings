from selenium import webdriver
from time import sleep, time
import requests
from bs4 import BeautifulSoup


URL = 'https://bookmaker-ratings.com.ua/ru/tips/today/'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'accept': '*/*'}

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


def get_bet_data(html):
    bet_info = {}
    soup = BeautifulSoup(html, 'html.parser')
    match = soup.find('div', class_='match-block')
#    bet_info['league'] = match.find('div', class_='league').text.strip()
    bet_info['date'] = match.find('div', class_='date').text.strip()
    bet_info['name'] = match.find('div', class_='name').text.strip()
    bet_info['bet'] = match.find('div', class_='bet-name').text.strip()
    print(bet_info)


def parser():
    time1 = time.time()
    start_link = URL
    match_list = get_match_list(get_html(start_link))
    print(len(match_list))
    for item in match_list:
        print('******************************************************************')
        print(item)
        get_bet_data(get_html(item))
    time2 = time.time()
    print('Work time: {}'.format(time2 - time1))



browser = webdriver.Firefox()
browser.implicitly_wait(5)
browser.get(URL)
try:
    close_btn = browser.find_element_by_class_name("close-button")
    sleep(2)
    close_btn.click()
except:
    print('no banner, go next step')

btn_more = browser.find_element_by_class_name("load_more-comments-text")
sleep(2)
btn_more.click()

sleep(2)

browser.get(URL)
requiredHtml = browser.page_source
print(requiredHtml)


parser()