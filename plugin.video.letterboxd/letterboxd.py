# Imports
from __future__ import division
import re
import requests

from BeautifulSoup import BeautifulSoup as soup
from xbmcswift2 import download_page


# Variables
URL_MAIN            = 'http://www.letterboxd.com'
URL_PAGE            = '/page/%s'
URL_USER            = URL_MAIN + '/%s'
URL_USER_DIARY      = URL_USER + '/films/diary'
URL_USER_WATCHLIST  = URL_USER + '/watchlist' + URL_PAGE
URL_USER_LISTS      = URL_USER + '/lists'
URL_USER_LIST       = URL_USER + '/list/%s' + URL_PAGE
URL_USER_FOLLOWING  = URL_USER + '/following'
URL_USER_FOLLOWERS  = URL_USER + '/followers'


# Get diary
def get_diary(username, page):
    films = []
    
    # Get data
    url = (URL_USER_DIARY + URL_PAGE) % (username, page)
    print url
    data = soup(download_page(url))
    
    if not data.find('h2', {'class':'ui-block-heading'}):
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
    
    
# Get lists
def get_lists(username, page):
    # Lists
    url = (URL_USER_LISTS) % (username)
    data = soup(download_page(url))
    data = data.findAll('div', {'class':'film-list-summary'})
    
    lists = [{
        'title':list.find('h2').text,
        'count':list.find('small').text.split('&')[0],
        'slug':list.find('a')['href'].split('/')[-2]
    } for list in data]
    
    # Return
    return lists
   
   
# Get list
def get_list(username, slug, page):
    # Films
    url = (URL_USER_WATCHLIST) % (username, page) if slug == 'watchlist' else (URL_USER_LIST) % (username, slug, page)
    data = soup(download_page(url))
    data = data.findAll('li', {'class':'poster-container'})
    
    films = [{
        'title':re.sub(r'\((.+)\)', ' ', film.find('a', {'class':'frame'})['title']).strip(),
        'year':re.search(r'\(([0-9]{4})\)', film.find('a', {'class':'frame'})['title']).group(1),
        'poster':film.find('img')['src']
    } for film in data]
    
    # Return
    return films
    

# ============= Network ======================================================================

# Get following
def get_following(username):
    # People
    people = []
    
    # Get data
    url = (URL_USER_FOLLOWING) % (username)
    data = soup(download_page(url))
    data = data.findAll('td', {'class':'table-person'})
    
    for person in data:
        name = person.find('h3', {'class':'name-heading'}).text
        username = person.find('h3', {'class':'name-heading'}).find('a')['href'].replace('/', '')
        avatar = person.find('img')['src']

        people.append({
            'name':name,
            'username':username,
            'avatar':avatar
        })

    # Return
    return people

    
# Get followers
def get_followers(username):
    people = []
    
    # Get data
    url = (URL_USER_FOLLOWERS) % (username)
    data = soup(download_page(url))
    data = data.findAll('td', {'class':'table-person'})
    
    for person in data:
        name = person.find('h3', {'class':'name-heading'}).text
        username = person.find('h3', {'class':'name-heading'}).find('a')['href'].replace('/', '')
        avatar = person.find('img')['src']

        people.append({
            'name':name,
            'username':username,
            'avatar':avatar
        })

    # Return
    return people
    



#print get_list('petterhj', 'wishlist', '1')