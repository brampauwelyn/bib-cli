######################################################
#
# bib-cli - search your local library
# written by Bram Pauwelyn 
#
######################################################

# import libraries

import urllib3
from bs4 import BeautifulSoup

local_library = input("Local Library? (e.g. Halle)")
search_query = input("What are you looking for? (e.g. Permaculture)")
url = 'zoeken.{}.bibliotheek.be/?q={}'.format(local_library, search_query)

http = urllib3.PoolManager()
response = http.request('GET', url)
soup = BeautifulSoup(response.data, 'html.parser')
results_container = soup.find('ol', attrs={'id': 'resultContainer'})
books = results_container.find_all('li')

for book in books:
  title = book.find('h2', attrs={'class': 'heading'}).text
  authors = book.find_all('span', attrs={'class': 'core-author'})
  print(len(authors))
  print(title)
