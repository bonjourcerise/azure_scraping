import pandas as pd
from bs4 import BeautifulSoup
import requests


# loop all the page baby
def all_page_link(start_url):
    all_urls = []
    url = start_url
    while(url != None):            
        all_urls.append(url)
        soup = BeautifulSoup(requests.get(url).text,"html.parser")
        next_links = soup.find_all(class_='next')
        if (len(next_links) == 0):        
            url = None
        else:
            next_page = "https://www.manucurist.com/" + next_links[0].find('a').get('href')
            url = next_page
    return all_urls

link = all_page_link('https://www.manucurist.com/collections/vernis-green?page=1')

def scrapping(url,class_):

    response = requests.get(url)
    page_contents = response.text
    soup = BeautifulSoup(page_contents, 'html.parser')
    goodsoup = soup.find_all("div", {"class": class_})
    
    mydata=[]

    for soup in goodsoup:
        title = soup.find("div", {"class": 'grid-product__title'}).text
        category = soup.find("div", {"class": 'grid-product__type'}).text.strip()
        price = soup.find("div", {"class": 'grid-product__price'}).text.strip()
        stock = soup.find("div", {"class": 'product__inventory'}).text.strip()
        
        products_dict = {
        'title': title,
        'category': category,
        'price': price,
        'stock': stock}
        
        mydata.append(products_dict)
    
    return mydata

data=[]

for i in link:
    data.extend(scrapping(i,"grid-product__content"))
df = pd.DataFrame(data)

df['price']=df['price'].str.replace('€','')
df['price']=df['price'].str.replace(',','.')
df['stock']=df['stock'].str.replace(' en stock','')

df.to_csv('manucurist.csv', index=None)
