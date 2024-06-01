

import requests
from bs4 import BeautifulSoup
import csv

def get_html(url):
    response = requests.get(url)
    return response.text

def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    list_page = soup.find('ul', class_ = 'pagination').find_all('li')
    last_page = list_page[-1]
    total_pages = last_page.find('a').get('href').split('=')
    return int(total_pages[-1])


def write_to_csv(data):
    with open('mashina_kg.csv','a') as f:
        writer = csv.writer(f)
        writer.writerow([data['title'],data['price'],data['img'],data['description']])


def get_title(html):
    soup = BeautifulSoup(html,'lxml')
    block_titles = soup.find_all('div', class_ = 'list-item list-label')
    # a = []
    for titles in block_titles:
        try:
            title = titles.find('div', class_='block title').find('h2',class_ = 'name').text.strip()
        except:
            title = ''
        try:
            price = titles.find('div',class_ ='block price').find('p').find('strong').text
        except:
            price = ''
        try:
            img = titles.find('img').get('data-src')
        except:
            img = ''
        try:
            description = titles.find('div', class_ ='block info-wrapper item-info-wrapper').find('p',class_ ='year-miles').text.strip()
        except:
            description = ''
        
        data = {'title': title, 'price':price, 'img':img, 'description':description}
        write_to_csv(data)

def main():
    url_ = 'https://www.mashina.kg/search/all/'
    pages ='?page='
    html_ = get_html(url_)
    number = get_total_pages(html_)

    for i in range(1, number+1):
        url_pages = url_ + pages + str(i)
        html = get_html(url_pages)
        get_title(html)
   
# Это было сложно :((

main()


