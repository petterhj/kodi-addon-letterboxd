# Imports
from __future__ import division
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
URL_USER_FOLLOWING = URL_USER + '/following'

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
        rating = (int(film.find('meta', {'itemprop':'rating'})['content']) / 2)
        liked = True if film.find('span', {'class':'has-icon icon-16 large-liked icon-liked'}) else False
        rewatch = False if film.find('td', {'class':'td-rewatch center icon-status-off'}) else True
        poster = film.find('img')['src']
        
        films.append({
            'title':title, 
            'year':year, 
            'watched':watched, 
            'rating':rating, 
            'liked':liked, 
            'rewatch':rewatch,
            'poster':poster
        })
        
    # Return
    return films
    
    
# Get user watchlist
def get_user_watchlist():
    films = []
    
    # Get data
    data = soup(download_page(URL_USER_WATCHLIST))
    data = data.findAll('li', {'class':'poster-container'})
    
    for film in data:
        title =  re.sub(r'\((.+)\)', ' ', film.find('a', {'class':'frame'})['title']).strip()
        year = re.search(r'\(([0-9]{4})\)', film.find('a', {'class':'frame'})['title']).group(1)
        poster = film.find('img')['src']
        
        films.append({
            'title':title,
            'year':year, 
            'poster':poster
        })

    # Return
    return films
    
    
# Get user lists
def get_user_lists(username):
    pass
    
    
# Get user following
def get_user_following():
    people = []
    
    # Get data
    data = soup(download_page(URL_USER_FOLLOWING))
    data = data.findAll('td', {'class':'table-person'})
    
    for person in data:
        name = person.find('h3', {'class':'name-heading'}).text
        avatar = person.find('img')['src']

        people.append({
            'name':name,
            'avatar':avatar
        })

    # Return
    return people

    



films = get_user_following()