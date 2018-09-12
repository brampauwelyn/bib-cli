######################################################
#
# bib-cli - search your local library
# written by Bram Pauwelyn 
#
######################################################

# import libraries

import urllib3
from urllib.parse import urlencode, quote_plus
from bs4 import BeautifulSoup
import emoji

# welcome screen

welcome_text = """
  ____ _____ ____     _____ _      _____ 
 |  _ \_   _|  _ \   / ____| |    |_   _|
 | |_) || | | |_) | | |    | |      | |  
 |  _ < | | |  _ <  | |    | |      | |  
 | |_) || |_| |_) | | |____| |____ _| |_ 
 |____/_____|____/   \_____|______|_____|
                                         
"""

print(welcome_text)

# ask for user input

local_library = input("Local Library? (e.g. Halle)")
search_query = input("What are you looking for? (e.g. Permaculture)")
main_url = 'zoeken.{}.bibliotheek.be'.format(local_library)
search_query = {'q': search_query}
search_query = urlencode(search_query, quote_via=quote_plus)
search_url = main_url + '/?{}'.format(search_query)

# make request and get results 

http = urllib3.PoolManager()
response = http.request('GET', search_url)
soup = BeautifulSoup(response.data, 'html.parser')
results_container = soup.find('ol', attrs={'id': 'resultContainer'})
books = results_container.find_all('li')

# output results 

print("""
===================================
            RESULTS
===================================
""")

for book in books:
  title = book.find('h2', attrs={'class': 'heading'}).text
  authors = book.find_all('span', attrs={'class': 'core-author'})
  authornames = ''
  for author in authors:
    authorname = author.find('span').text
    authornames += '| {}'.format(authorname) if authornames  else '{} '.format(authorname)
  booktype = book.find('span', attrs={'class': 'material-text'})
  booktype = booktype.text if booktype is not None else '/'
  language = book.find('span', attrs={'class': 'short-details-language'}).text
  detail_link = book.find('a', attrs={'class': 'detaillink'}).get('href')
  detail_url = main_url + detail_link
  detail_response = http.request('GET', detail_url)
  detail_soup = BeautifulSoup(detail_response.data, 'html.parser')
  isbn = detail_soup.find('dd', attrs={'itemprop': 'isbn'})
  isbn = isbn.text if isbn is not None else '/'
  availitems = detail_soup.find('ul', attrs={'class': 'avail-items'})
  availitems = availitems.find('ul')
  availitems = availitems.find_all('li', attrs={'class': 'avail-item'})
  print('Title: {}'.format(title))
  print('Author: {}'.format(authornames))
  print('Type: {}'.format(booktype))
  print('Language: {}'.format(language))
  print('ISBN: {}'.format(isbn))
  # print('Available: ')
  # for availitem in availitems:
  #   icon = availitem.find('i', attrs={'class': 'avail-icon-loanedout'})
  #   icon = ':red_circle:' if icon is None else ':+1:'
  #   print(emoji.emojize(icon, use_aliases=True))
  print("===================================")
