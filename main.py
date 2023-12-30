#made by joel hellums
#takes in a list of local html files to scrape (taken from sherwin-williams.com) and returns a list of links to all SDSs

import re #regex
import urllib.request #grabs urls
#import urllib.parse #urllib acts up if links arent put through this
from bs4 import BeautifulSoup #html scraper

import _thread

#find all links to products in site
def scrape_site(page):
    file = open('pagelinks.txt', 'a')

    #get all product links in site
    soup = BeautifulSoup(page, 'lxml')
    product_names = soup.find_all('h3', class_='prod-shelf__product__title')
    for product in product_names:
            product_link = 'https://www.sherwin-williams.com' + product.a['href']
            file.write(product_link)
            file.write('\n')
    
    file.close()

#return an html page from the internet
def get_page(quote_page):
    page = urllib.request.urlopen(quote_page)
    return page

#return a local html page
def get_page_local(quote_page): 
    file = open(quote_page, 'r')
    page = file.read()
    file.close
    return page

def getsdslinks(quote_page):
    #gets page and puts it into a string
    #quote_page = 'https://www.sherwin-williams.com/painting-contractors/products/scuff-tuff-interior-waterbased-enamel'
    page = get_page(quote_page)
    soup = BeautifulSoup(page, 'lxml')

    #finds all 12 digit numbers in the page (dumb, but it works)
    magic_numbers = re.findall('\d\d\d\d\d\d\d\d\d\d\d\d', str(soup))

    #check for all repeats and remove them, this thing is slow enough as is
    magic_numbers_truncated = list(dict.fromkeys(magic_numbers))
    print(magic_numbers_truncated)

    #check if link is valid and print to file if it is

    for numbers in magic_numbers_truncated:
        #checknumber(numbers)
        _thread.start_new_thread(checknumber, (numbers,))
        
        
def checknumber(number):
    file = open('sdslinks.txt', 'a')
    page_url = 'https://www.sherwin-williams.com/document/SDS/en/' + str(number) + '/US/'

            #check if 404
    try:
        conn = urllib.request.urlopen(page_url)
    except urllib.error.HTTPError as e:
            # Return code error (e.g. 404, 501, ...)
            # ...
        print('HTTPError: {}'.format(e.code))
    except urllib.error.URLError as e:
            # Not an HTTP-specific error (e.g. connection refused)
            # ...
        print('URLError: {}'.format(e.reason))
    else:
            # 200
            # ...
        print(page_url)
        file.write(page_url)
        file.write('\n')
    file.close()


#read all lines in a text file as a list
def readsplitfile(filename):
    file = open(filename, 'r')
    linklist = str.split(file.read())
    file.close()
    return linklist

#main
#scrape local html files for links to products
mainlinklist = readsplitfile('mainlinks.txt')
print('reading main file')
for link in mainlinklist:
    print(link)
    page = get_page_local(link)
    scrape_site(page)
    print('scraped file', link)

#scrape page links for SDSs
pagelinklist = readsplitfile('pagelinks.txt')
pagelinklist = list(dict.fromkeys(pagelinklist)) #remove duplicates from list (remove this line if problems occur)
print('reading page links')
for link in pagelinklist:
    print(link)
    getsdslinks(link)
    print('scraped page', link)

print('done')
