# Imports
import re
import requests

from BeautifulSoup import BeautifulSoup as soup
from xbmcswift2 import download_page


# Variables
USERNAME = 'petterhj'

URL_MAIN = 'http://www.letterboxd.com'
URL_USER = URL_MAIN + '/' + USERNAME
URL_USER_DIARY = URL_USER + '/films/diary/page/'
URL_USER_WATCHLIST = URL_USER + '/watchlist'

# Get diary entries
def get_user_diary(page=1):
    films = []
    
    # Get data
    data = soup(download_page(URL_USER_DIARY + str(page)))
    data = data.find('table', {'id':'diary-table'})
    data = data.findAll('tr', {'class':'diary-entry-row'})
    
    for film in data:
        title = film.find('h3', {'class':'film-title prettify'}).text
        year = film.find('td', {'class':'td-released center'}).text
        watched = film.find('td', {'class':'td-day diary-day center'})
        watched = '.'.join(reversed(watched.find('a')['href'].split('/')[-4:-1]))
        rating = film.find('meta', {'itemprop':'rating'})['content']
        liked = True if film.find('span', {'class':'has-icon icon-16 large-liked icon-liked'}) else False
        rewatch = False if film.find('td', {'class':'td-rewatch center icon-status-off'}) else True
        
        films.append({'title':title, 'year':year, 'watched':watched, 'rating':rating, 'liked':liked, 'rewatch':rewatch})
        
    # Return
    return films
    
    
# Get user watchlist
def get_user_watchlist():
    films = []
    
    # Get data
    data = soup(download_page(URL_USER_WATCHLIST))
    data = data.find('ul', {'class':'posters film-list clear posters-125 equalize'})
    data = data.findAll('a', {'class':'frame'})
    
    for film in data:
        title = re.sub(r'\((.+)\)', ' ', film['title']).strip()
        year = re.search(r'\(([0-9]{4})\)', film['title']).group(1)
        
        films.append({'title':title, 'year':year})

    # Return
    return films

    
# Get user lists
def get_user_lists(username):
    pass


#films = get_diary()