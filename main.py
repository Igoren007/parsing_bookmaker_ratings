import requests
import json
from bs4 import BeautifulSoup
from user_agent import generate_user_agent


TOKEN = '1799874715:AAE0Rj4-SpV-OMAxLZg3hhbKIIueYwXZ9oM'
CHANNEL = -1001337710941


# this function returns HTML page code
def get_html(url, params=None):
    ua = generate_user_agent()
    headers = {'User-Agent': ua}
    try:
        response = requests.get(url, headers=headers, params=params).text
    except:
        response = 'Error'

    return response


# this function returns a list of links to matches from this html page
def get_match_list(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='block-item iscroll-item has-image')
    more_btn = soup.find('a', class_='load_more-comments-text')
    links = []
    for item in items:
        link = item.a.get('href')
        links.append(link)
    return links, more_btn


# gets the required data from the page
def get_bet_data(html, link):

    soup = BeautifulSoup(html, 'html.parser')
    match = soup.find('div', class_='match-block')
    sport = soup.find('ul', class_='breadcrumbs').find_all('li')[2].text.split(' ')[-1]
    bet_data = {
        "sport": sport,
        "link": link,
        "date": match.find('div', class_='date').text.strip(),
        "title": match.find('div', class_='name').text.strip(),
        "bet": match.find('div', class_='bet-name').text.strip(),
        "kf": match.a.get('data-factor-dec')
    }
    return bet_data


def parser(url_base):

    bets = []
    more = True
    i = 1
    while more:
        url = f'{url_base}?paged={str(i)}'
        # если more=False значит кнопки "показать еще матчи" нет, следовательно мы прерывает цикл
        match_list, more = get_match_list(get_html(url))
        for item in match_list:
            bets.append(get_bet_data(get_html(item), item))
        i += 1
    return bets


if __name__ == '__main__':
    url_today = 'https://bookmaker-ratings.com.ua/ru/tips/today/'
    bets_today = parser(url_today)

    url_tommorow = 'https://bookmaker-ratings.com.ua/ru/tips/tomorrow/'
    bets_tommorow = parser(url_tommorow)
    bets = bets_today + bets_tommorow

    with open('bets.json', 'w') as f:
        json.dump(bets, f, ensure_ascii=False, separators=(',', ': '))
