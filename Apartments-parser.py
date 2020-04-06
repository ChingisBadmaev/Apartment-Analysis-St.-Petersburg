
import requests
from bs4 import BeautifulSoup
import csv


HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36', 'accept': '*/*'}

list_of_links = open("ListOfApartments.csv")
links = []
for link in list_of_links:
    link = link.replace('\n', '')
    links.append(link)
del links[0]


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find('div', class_='object__param').find_all('div', class_='object__param-item-name')
    for item in items:
        print(item.get_text())


def parse():
    signs = links
    for sign in signs:
        URL = sign
        html = get_html(URL)
        if html.status_code == 200:
            get_content(html.text)
            break


parse()



