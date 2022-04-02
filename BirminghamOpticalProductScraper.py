#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas as pd


# In[ ]:


headers = {
"User-Agent":"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36"
}

# Create a function to collect URLs from xml file
def get_urls_of_xml(xml_url):
    r = requests.get(xml_url)
    xml = r.text
    soup = BeautifulSoup(xml)

    links_arr = []
    for link in soup.findAll('loc'):
        linkstr = link.getText('', True)
        links_arr.append(linkstr)

    return links_arr

# Use created function on specific sitemap.xml
links_data_arr = get_urls_of_xml('https://www.birminghamoptical.co.uk/product-sitemap.xml')
links_data_arr.remove('https://www.birminghamoptical.co.uk/products/')

# Loop through all URLs to collect HTML tag data and store in a list
productlist = []
for link in links_data_arr:

    r = requests.get(link, headers=headers)

    soup = BeautifulSoup(r.content, 'lxml')

    name = soup.find('h1', class_='h3').text.strip()
    try:
        price = soup.find('span', class_='woocommerce-Price-amount amount').text.strip()
    except:
        price = "Enquire"
    try:
        sku = soup.find('span', class_='sku').text.strip()
    except:
        sku = "No SKU"
    try:
        description = soup.find('div', class_='product-overview').text.strip().replace("\n", " ").replace("At a glance: ", "")
    except:
        description = "No description"
    pageurl = soup.find('link', rel="canonical").get('href')

    # Create a dictionary entry to store list item
    product = {
        'name':name,
        'price':price,
        'sku':sku,
        'description':description,
        'pageurl':pageurl
    }
    
    productlist.append(product)
    #print('saving: '', product['name'])

# Create dataframe to store in a .csv
df = pd.DataFrame.from_dict(productlist)
df.head()

df.to_csv('BirminghamOpticalProducts.csv', encoding='utf-8-sig')


# In[ ]:




