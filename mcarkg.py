import csv
import requests
from bs4 import BeautifulSoup

def write_to_csv(data):
    with open('mashina_kg.csv', 'a', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter='/')
        writer.writerow([data['title'], data['price'], data['photo'], data['description']])

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    product_list = soup.find('div', class_="listing").find_all('div', class_="list-item list-label")
    
    for product in product_list:
        try:
            photo = product.find('img').get('data-src', '')
        except AttributeError:
            photo = ''

        try:
            title = product.find('h2').text.strip()
        except AttributeError:
            title = ''

        try:
            price = product.find('strong', class_="price").text.strip()
        except AttributeError:
            price = ''

        try:
            description = product.find('p').text.strip()
        except AttributeError:
            description = ''

        data = {'title': title, 'price': price, 'photo': photo, 'description': description}
        print(data)  
        write_to_csv(data)

def main():
    base_url = 'https://www.mashina.kg/search/all/'
    pages = 5 

    for page in range(1, pages + 1):
        url = f"{base_url}?page={page}"
        response = requests.get(url)
        if response.status_code == 200:
            get_page_data(response.text)
        else:
            print(f"Error: Unable to fetch page {page}")

if __name__ == "__main__":
    main()
