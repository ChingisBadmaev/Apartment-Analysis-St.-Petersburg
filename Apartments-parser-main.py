import requests
from bs4 import BeautifulSoup
import csv

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) '
                         'Chrome/80.0.3987.122 Safari/537.36', 'accept': '*/*'}

FILE = 'house.csv'


list_of_links = open("URL_list.csv")
links = []
for link in list_of_links:
    link = link.replace('\n', '')
    links.append(link)
count_district = len(links)


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='catalog-item__container')
    houses = []
    for item in items:
        title = item.find('div', class_='catalog-item__headline').get_text().replace('                            м2', ' м2')
        area = title.split(' ')[-2]
        type_of_housing = title.replace(area, '')

        # studio or apartment
        if len(type_of_housing.split(' ')) > 1:
            type_of_housing = type_of_housing.split(' ')[-3]
        else:
            type_of_housing = 'студия'

        # if there is price information
        if item.find('div', class_='catalog-item__price'):
            price = item.find('div', class_='catalog-item__price').get_text().replace('                                тыс. руб.\n                            ', ' 000 руб')
        else:
            price = ''

        # if there is metro name information
        if item.find('span', class_='catalog-item__metro-name'):
            metro_name = item.find('span', class_='catalog-item__metro-name').get_text().replace('\xa0', '')
        else:
            metro_name = ''

        # if there is information about the distance to the metro
        if item.find('span', class_='catalog-item__metro-distance'):
            metro_distance = item.find('span', class_='catalog-item__metro-distance').get_text(strip=True)
        else:
            metro_distance = ''

        # if there is information about the location of the apartment area
        if item.find('div', class_='catalog-item__district'):
            district = item.find('div', class_='catalog-item__district').get_text()
        else:
            district = ''
        # parse cards with the same class name
        many_characteristic = item.find_all('span', class_='catalog-item__param-value')
        i = int(0)
        j = int(0)
        for characteristic in many_characteristic:
            j = j + 1
        if j == 5:
            for characteristic in many_characteristic:
                if i == 0:
                    living_space = characteristic.get_text()
                if i == 2:
                    height = characteristic.get_text()
                if i == 3:
                    floor = characteristic.get_text()
                i = i + 1
        if j == 4:
            for characteristic in many_characteristic:
                if i == 0:
                    living_space = characteristic.get_text()
                if i == 2:
                    floor = characteristic.get_text()
                height = ''
                i = i + 1
        if j == 3:
            for characteristic in many_characteristic:
                if i == 0:
                    living_space = characteristic.get_text()
                if i == 1:
                    floor = characteristic.get_text()
                height = ''
                i = i + 1

        # add characteristics
        houses.append({
            'type_of_housing': type_of_housing,
            'area': area,
            'price': price,
            'metro_name': metro_name,
            'metro_distance': metro_distance,
            'district': district,
            'living_space': living_space,
            'ceiling_height': height,
            'floor': floor
        })
    return houses


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['Type of housing', 'Area', 'Price', 'Metro name', 'Metro distance', 'District', 'Living space',
                         'Ceiling height', 'Floor'])
        for item in items:
            writer.writerow([item['type_of_housing'], item['area'], item['price'], item['metro_name'],
                             item['metro_distance'], item['district'], item['living_space'], item['ceiling_height'],
                             item['floor']])


def parse():
    houses = []
    number_of_district = 1
    for URL in links:
        print(f' парсинг района {number_of_district} из {count_district}')
        html = get_html(URL)
        if html.status_code == 200:
            pages_count = int(17)
            for page in range(1, pages_count + 1):
                # print(f'Парсинг страницы {page} из {pages_count}')
                html = get_html(URL, params={'page': page})
                houses.extend(get_content(html.text))
            save_file(houses, FILE)
        else:
            print('Error')
        number_of_district = number_of_district + 1


parse()
