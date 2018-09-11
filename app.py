######################################################
#
# bib-cli - search your local library
# written by Bram Pauwelyn 
#
######################################################

# import libraries

import urllib3
from bs4 import BeautifulSoup

# welcome screen


# ask for user input

local_library = input("Local Library? (e.g. Halle)")
search_query = input("What are you looking for? (e.g. Permaculture)")
main_url = 'zoeken.{}.bibliotheek.be'.format(local_library)
search_url = main_url + '/?q={}'.format(search_query)

# make request and get results 

http = urllib3.PoolManager()
response = http.request('GET', search_url)
soup = BeautifulSoup(response.data, 'html.parser')
results_container = soup.find('ol', attrs={'id': 'resultContainer'})
books = results_container.find_all('li')

# output results 

for book in books:
  title = book.find('h2', attrs={'class': 'heading'}).text
  authors = book.find_all('span', attrs={'class': 'core-author'})
  authornames = ''
  for author in authors:
    authorname = author.find('span').text
    authornames += '| {}'.format(authorname) if authornames  else '{} '.format(authorname)
  detail_link = book.find('a', attrs={'class': 'detaillink'}).get('href')
  detail_url = main_url + detail_link
  # print(detail_url)
  detail_response = http.request('GET', detail_url)
  detail_soup = BeautifulSoup(detail_response.data, 'html.parser')
  # print(detail_soup)
  isbn = detail_soup.find('dd', attrs={'itemprop': 'isbn'}).text
  print('Author: {}'.format(authornames))
  print('Title: {}'.format(title))
  print('ISBN: {}'.format(isbn))
  print("===================================")
