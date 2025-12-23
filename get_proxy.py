"""
    █▀▀ █▀▀ ▀█▀ ▄▄ █▀█ █▀█ █▀█ ▀▄▀ █▄█
    █▄█ ██▄ ░█░ ░░ █▀▀ █▀▄ █▄█ █░█ ░█░
a simple code for parsing 1000+ free proxies
            ｂｙ ｂ１ｔ０ｎｅ
        tg: https://t.me/w0rld_adm1n
    github: https://github.com/b1t0nese
"""

import requests
from bs4 import BeautifulSoup


def get_page_data(html):
    soup = BeautifulSoup(html, "html.parser")
    line = soup.find('table', class_='style_table__YadoX').find('tbody').find_all('tr')

    proxys = []
    for tr in line:
        td = tr.find_all('td')
        adress = td[5].text+'://'+td[0].text+':'+td[1].text
        country = td[4].text
        anonym = td[6].text
        time = td[10].text.replace(' ', '').replace('мс', '')

        data = {'Адрес': adress,
                'Страна': country,
                'Анонимность': anonym,
                'Пинг (мс)': time}
        proxys.append(data)

    return [item for item in proxys
              if item['Анонимность']=='Высокая'
              and int(item['Пинг (мс)'])<=200]


def get_proxys(pr_count, country_filter):
    proxys = []
    page = 1
    while len(proxys)<pr_count:
        url = 'https://proxyfreeonly.com/ru/free-proxy-list?page='+str(page)
        proxys += get_page_data(requests.get(url).text)
        if not country_filter:
            proxys = proxys
        else:
            proxys = [proxy for proxy in proxys if proxy['Страна'] == country_filter.upper()]
        page += 1

    return proxys


if __name__ == '__main__':
    pc = int(input("Введите количевство нужных прокси: "))
    cf = input("Введите страну для фильтрации (или пропустите этот момент для полного списка): ")
    proxys = get_proxys(pc, cf)
    proxy_strings = [f"Адрес: {item['Адрес']}, Страна: {item['Страна']}, Анонимность: {item['Анонимность']}, Пинг: {item['Пинг (мс)']} мс" for item in proxys]
    print(f'\nНайдено {len(proxy_strings)} прокси:')
    print('\n'.join(proxy_strings))
