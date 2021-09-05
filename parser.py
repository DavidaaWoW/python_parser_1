from os import write
import requests
from bs4 import BeautifulSoup
import csv
import re

URL = 'https://www.avtomaxi.ru/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 YaBrowser/21.6.4.693 Yowser/2.5 Safari/537.36'}
HOST = 'https://www.avtomaxi.ru'
cars = []

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def somefunc(tag):
    if tag.has_attr('itemprop') and tag.has_attr('src'):
        return True
    else:
        return False

def somefunc1(tag):
    if tag.has_attr('itemprop') and tag.has_attr('href'):
        return True
    else:
        return False

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='result-car-block')
    
    for item in items:
        curr_link = HOST + item.find('span', class_='h2').find_next('a').get('href')
        html2 = get_html(curr_link)
        soup2 = BeautifulSoup(html2.text, 'html.parser')
        description = soup2.find('div', class_='txt')
        if description:
            description = description.get_text(strip=True)
        else:
            description = soup2.find('h4', text='Краткое описание:').find_next('p').get_text(strip=True)
        col3 = soup2.find_all('div', class_='other-select-col')
        rent_price = soup2.find_all('div', class_='result-car-col-info-table-col')
        a = 0
        for num in rent_price:
            rent_price[a] = num.find_next('span', class_='price-day').find_next('span', class_='new').get_text()
            a+=1
        a = 0
        rent_terms = soup2.find('ul', class_='rent_terms').find_all('li')
        for num in rent_terms:
            rent_terms[a] = num.get_text(strip=True)
            a += 1
        a = 0
        default_hide = soup2.find('div', class_='additional_info').find_all('p')
        characheristics1 = soup2.find_all('div', class_='characteristic-col')
        ch0 = characheristics1[0].find_next('ul').find_all('li')
        for num in ch0:
            k = num.find_all('span')
            ch0[a] = k[1].get_text()
            a += 1
        a = 0
        if len(ch0) == 6:
            char = ch0[5]
        else:
            char = ''
        ch1 = characheristics1[1].find_next('ul').find_all('li')
        for num in ch1:
            k = num.find_all('span')
            ch1[a] = k[1].get_text()
            a += 1
        a = 0
        checkbox = soup2.find_all('label', class_='col-services-checkbox')
        
        images = soup2.find_all(somefunc)
        for num in images:
            images[a] = num.get('src')
            a+=1
        a = 0

        clas = soup2.find_all(somefunc1)
        clas[1] = clas[1].find_next('span').get_text()
        cars.append({
            'title': item.find('span', class_='h2').get_text(strip = True),
            'img_link': HOST + item.find('span', class_='img-car-t').find_next('span').find_next('img').get('src'),
            'car_link': curr_link,
            'brand': soup2.find('div', class_='marka').find_next('p').find_next('a').get_text(),
            'year': soup2.find('div', class_='marka').find_next('p').find_next('span', class_='year').find_next('b').get_text(),
            'description': description,
            'people': col3[0].find_next('b').get_text(),
            'doors': col3[1].find_next('b').get_text(),
            'transmission': col3[2].find_next('b').get_text(),
            '1-2': rent_price[0],
            '3-6': rent_price[1],
            '7-14': rent_price[2],
            '15-30': rent_price[3],
            '1-2m': rent_price[4],
            'deposit': rent_price[5],
            'rt1': rent_terms[0],
            'rt2': rent_terms[1],
            'rt3': rent_terms[2],
            'rt4': rent_terms[3],
            'rt5': rent_terms[4],
            'rt6': rent_terms[5],
            'limit': default_hide[1].get_text(),
            'orun': default_hide[2].get_text().replace('₽', 'P'),
            'ch1': ch0[0],
            'ch2': ch0[1],
            'ch3': ch0[2],
            'ch4': ch0[3],
            'ch5': ch0[4],
            'ch6': char,
            'ch11': ch1[0],
            'ch12': ch1[1],
            'ch13': ch1[2],
            'ch14': ch1[3],
            'ch15': ch1[4],
            'nolimit': checkbox[2].find_next('p').find_next('span').get_text().replace(' ₽ / сутки', ''),
            'fullprotect': checkbox[3].find_next('p').find_next('span').get_text().replace(' ₽ / сутки', ''),
            'img1': HOST + images[0],
            'img2': HOST + images[1],
            'img3': HOST + images[2],
            'img4': HOST + images[3],
            'img5': HOST + images[4],
            'img6': (HOST + images[5] if len(images) > 5 else ''),
            'img7': (HOST + images[6] if len(images) > 6 else ''),
            'img8': (HOST + images[7] if len(images) > 7 else ''),
            'img9': (HOST + images[8] if len(images) > 8 else ''),
            'img10': (HOST + images[9] if len(images) > 9 else ''),
            'img11': (HOST + images[10] if len(images) > 10 else ''),
            'img12': (HOST + images[11] if len(images) > 11 else ''),
            'img13': (HOST + images[12] if len(images) > 12 else ''),
            'img14': (HOST + images[13] if len(images) > 13 else ''),
            'img15': (HOST + images[14] if len(images) > 14 else ''),
            'class': clas[1].replace('Прокат автомобилей ', '').replace(' класс', ''),
        })
        print(cars)

def save_file(items,path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Заголовок', 'Ссылка на изображение', 'car link', 'Марка', 'Год', 'Описание', 'Кол-во людей', 'Кол-во дверей', 'Коробка передач', '1-2 дня', '3-6 дней', '7-14 дней', '15-30 дней', '1-2 месяца', 'Залог', 'rt1', 'rt2', 'rt3', 'rt4', 'rt5', 'rt6', 'limit', 'orun', 'ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6', 'ch11', 'ch12', 'ch13', 'ch14', 'ch15', 'nolimit', 'fullprotect', 'img1', 'img2', 'img3', 'img4', 'img5', 'img6', 'img7', 'img8', 'img9', 'img10', 'img11', 'img12', 'img13', 'img14', 'img15', 'class'])
        for item in items:
            writer.writerow([item['title'], item['img_link'], item['car_link'], item['brand'], item['year'], item['description'], item['people'], item['doors'], item['transmission'], item['1-2'], item['3-6'], item['7-14'], item['15-30'], item['1-2m'], item['deposit'], item['rt1'], item['rt2'], item['rt3'], item['rt4'], item['rt5'], item['rt6'], item['limit'], item['orun'], item['ch1'], item['ch2'], item['ch3'], item['ch4'], item['ch5'], item['ch6'], item['ch11'], item['ch12'], item['ch13'], item['ch14'], item['ch15'], item['nolimit'], item['fullprotect'], item['img1'], item['img2'], item['img3'], item['img4'], item['img5'], item['img6'], item['img7'], item['img8'], item['img9'], item['img10'], item['img11'], item['img12'], item['img13'], item['img14'], item['img15'], item['class'],])

def parse():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
        save_file(cars, 'cars.csv')
        print('Success!')
    else:
        print('Error')

parse()