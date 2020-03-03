import requests
from bs4 import BeautifulSoup

MAIN_URL = 'https://www.bn.ru/kvartiry-vtorichka/?kkv=&pricePer=1&priceFrom=&priceTo=&squareFrom=&squareTo' \
           '=&squareLivingFrom=&squareLivingTo=&squareKitchenFrom=&squareKitchenTo=&distanceToMetro=0&typeHouseGroup' \
           '=&floorFrom=&floorTo=&balcony=0&elevator=0&notFirstFloor=0&onlyFirstFloor=0&notLastFloor=0&onlyLastFloor' \
           '=0&district%5B%5D=1&district%5B%5D=2&district%5B%5D=10&district%5B%5D=13&district%5B%5D=3&district%5B%5D' \
           '=4&district%5B%5D=5&district%5B%5D=6&district%5B%5D=7&district%5B%5D=8&district%5B%5D=9&district%5B%5D=11' \
           '&district%5B%5D=12&district%5B%5D=15&district%5B%5D=16&district%5B%5D=17&district%5B%5D=19&district%5B%5D' \
           '=20&search_geo_v3=&search_he=&search_he_dev= '
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/80.0.3987.122 Safari/537.36', 'accept': '*/*'}
HOST = 'https://www.bn.ru/'


# 1
def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def links_to_apartments(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a', class_='catalog-item__action-more')
    home_links = []
    for item in items:
        home_links.append({
            'link': HOST + item.get('href')
        })
        print()
    print(home_links)
    print(len(home_links))


# 2
def parse():
    html = get_html(MAIN_URL)
    if html.status_code == 200:
        links_to_apartments(html.text)


parse()

