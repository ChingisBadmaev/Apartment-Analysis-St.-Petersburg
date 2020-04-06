import requests
from bs4 import BeautifulSoup

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/80.0.3987.122 Safari/537.36', 'accept': '*/*'}
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
    itemsName = soup.find('div', class_='object__param').find_all('div', class_='object__param-item-name')
    # metroName = soup.find('div', class_='object__transport').find_next('span',
    # class_='object__transport-metro-name').get_text()
    characteristicsName = []
    for item in itemsName:
        characteristicsName.append(item.get_text())
    characteristicsName.append('Ближайшее метро')
    characteristicsName.append('Расстояние до ближайшего метро')

    house = []
    itemsValue = soup.find('div', class_='object__param').find_all('div', class_='object__param-item-value')
    i = int(0)
    for item in itemsValue:
        house.append({
            characteristicsName[i]: item.get_text()
        })
        i = i + 1
    house.append({
        'Ближайшее метро': soup.find('span', class_='object__transport-metro-name').get_text(),
        'Расстояние до ближайшего метро': soup.find('span', class_='object__transport-distance').get_text()
    })
    print(house)


def parse():
    for link in links:
        URL = link
        html = get_html(URL)
        if html.status_code == 200:
            get_content(html.text)


parse()
