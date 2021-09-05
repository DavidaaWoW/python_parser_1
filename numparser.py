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
            '1-2': (rent_price[0] if rent_price[0] != '-' else 0),
            '3-6': rent_price[1],
            '7-14': rent_price[2],
            '15-30': rent_price[3],
            '1-2m': rent_price[4],
            'deposit': rent_price[5],
        })
        print(cars)

def save_file(items,path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Заголовок', 'days', 'price'])
        for item in items:
            for some in range(1,3):
                writer.writerow([item['title'], some, item['1-2'], ])
            for some in range(3,7):
                writer.writerow([item['title'], some, item['3-6'], ])
            for some in range(7,15):
                writer.writerow([item['title'], some, item['7-14'], ])
            for some in range(15,31):
                writer.writerow([item['title'], some, item['15-30'], ])
            for some in range(31,61):
                writer.writerow([item['title'], some, item['1-2m'], ])

def parse():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
        save_file(cars, 'cars2.csv')
        print('Success!')
    else:
        print('Error')

parse()