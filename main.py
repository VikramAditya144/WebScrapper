from bs4 import BeautifulSoup as bs
import requests
from tabulate import tabulate

header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0", 
           "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8"}

name = input('Enter product name: ')

page = requests.get(headers=header, url="https://www.flipkart.com/search?q=" + name)

soup = bs(page.content, 'html5lib')

# Flipkart

method = 1
page = soup.find('div', attrs={'class':'_36fx1h _6t1WkM _3HqJxg'})

if (page.find('div', attrs={'class':'_2kHMtA'}) != None):
    method = 2
elif (page.find('a', attrs={'class':'IRpwTa'}) != None):
    method = 3

if (method == 1):
    products = soup.findAll('div', attrs={'class':'_4ddWXP'})
elif (method == 2):
    products = soup.findAll('div', attrs={'class':'_2kHMtA'})
elif (method == 3):
    products = soup.findAll('div', attrs={'class':'_2B099V'})

output = []
for product in products:
    if (product.find('div', attrs={'class':'_30jeq3'}) != None):
        if (method == 1):
            output.append([product.find('a', attrs={'class':'s1Q9rs'})['title'], product.find('div', attrs={'class':'_30jeq3'}).text])
        elif (method == 2):
            output.append([product.find('div', attrs={'class':'_4rR01T'}).text, product.find('div', attrs={'class': '_30jeq3'}).text])
        elif (method == 3):
            output.append([product.find('a', attrs={'class':'IRpwTa'})['title'], product.find('div', attrs={'class': '_30jeq3'}).text])

if (len(output) != 0):
    print("\nFlipkart:\n")
    print(tabulate(output, headers=['Product', 'Price'], tablefmt='grid', maxcolwidths=[100, None]))

# Amazon

page = requests.get(headers=header, url="https://www.amazon.in/s?k=" + name)

soup = bs(page.content, 'html5lib')

method = 1
page = soup.find('div', attrs={'id': 'search'})
if (page.find('div', attrs={'class':'a-section a-spacing-small a-spacing-top-small'}) != None):
    method = 1
elif (page.find('div', attrs={'class':'a-section a-spacing-small puis-padding-left-small puis-padding-right-small'}) != None):
    method = 2

if (method == 1):
    products = soup.findAll('div', attrs={'class':'a-section a-spacing-small a-spacing-top-small'})
elif (method == 2):
    products = soup.findAll('div', attrs={'class', 'a-section a-spacing-small puis-padding-left-small puis-padding-right-small'})

output = []
for product in products:
    if (method == 1):
        if (product.find('span', attrs={'class':'a-size-medium a-color-base a-text-normal'}) != None and product.find('span', attrs={'class':'a-offscreen'}) != None):
            output.append([product.find('span', attrs={'class':'a-size-medium a-color-base a-text-normal'}).text, product.find('span', attrs={'class':'a-offscreen'}).text])
    elif (method == 2):
        if (product.find('span', attrs={'class':'a-size-base-plus a-color-base'}) != None and product.find('span', attrs={'class':'a-size-base-plus a-color-base a-text-normal'}) != None and product.find('span', attrs={'class':'a-offscreen'}) != None):
            output.append([product.find('span', attrs={'class':'a-size-base-plus a-color-base'}).text + " " + product.find('span', attrs={'class':'a-size-base-plus a-color-base a-text-normal'}).text, product.find('span', attrs={'class':'a-offscreen'}).text])

if (len(output) != 0):
    print("\n\nAmazon\n")
    print(tabulate(output, headers=['Product', 'Price'], tablefmt='grid', maxcolwidths=[100, None]))