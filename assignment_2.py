import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = 'https://books.toscrape.com/'
response = requests.get(URL)
page_contents = response.text


doc = BeautifulSoup(page_contents, 'html.parser')

def get_book_titles(doc):
    Book_title_tags = doc.find_all('h3')
    Book_titles = []
    for tags in Book_title_tags:
        Book_titles.append(tags.text)
    return Book_titles

def get_book_price(doc):
    Book_price_tags = doc.find_all('p', class_ = 'price_color')
    Book_price = []
    for tags in Book_price_tags:
        Book_price.append(tags.text.replace('Â',''))
    return Book_price

def get_stock_availability(doc):
    Book_stock_tags = doc.find_all('p', class_ = 'instock availability')
    Book_stock = []
    for tags in Book_stock_tags:
        Book_stock.append(tags.text.strip())
    return Book_stock

def get_doc(url):
    response = requests.get(url)
    doc = BeautifulSoup(response.text,'html.parser')
    if response.status_code != 200:
        raise Exception('Failed to load page {}'.format(response))
    return doc

def scrape_multiple_pages(n):
    URL = 'https://books.toscrape.com/catalogue/page-'
    titles,prices,stocks_availability,urls = [],[],[],[]
    
    for page in range(1,n+1):
        doc = get_doc(URL + str(page)+ '.html')
        titles.extend(get_book_titles(doc))
        prices.extend(get_book_price(doc))
        stocks_availability.extend(get_stock_availability(doc))
        
    book_dict1 = {
                'TITLE':titles,
                'PRICE':prices,
                'STOCK AVAILABILTY':stocks_availability
    }
    return pd.DataFrame(book_dict1)
    
df = pd.DataFrame(scrape_multiple_pages(50)) 
df.to_csv('C:\\Users\\VIHAAN\\Documents\\projects\\assignment_2.csv', index=False, encoding='utf-8')
