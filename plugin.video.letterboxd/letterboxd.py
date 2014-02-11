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
URL_USER_DIARY      = URL_USER + '/films/diary' + URL_PAGE
URL_USER_WATCHLIST  = URL_USER + '/watchlist' + URL_PAGE
URL_USER_LISTS      = URL_USER + '/lists' + URL_PAGE
URL_USER_LIST       = URL_USER + '/list/%s' + URL_PAGE
URL_USER_FOLLOWING  = URL_USER + '/following' + URL_PAGE
URL_USER_FOLLOWERS  = URL_USER + '/followers' + URL_PAGE

URL_FILMS           = URL_MAIN + '/films'
URL_FILMS_GENRE     = URL_FILMS + '/%s'


# ============= Profile ======================================================================

# Get profile
def get_profile(username):    
    # Profile
    data = _getData((URL_USER) % (username))[0]
    
    stats = data.find('ul', {'class':'stats'}).findAll('strong')
    stats = {'film': stats[0].text, 'this_year': stats[1].text, 'lists': stats[2].text, 'following': stats[3].text, 'followers': stats[4].text}
    
    # Return
    return stats


# ============= Diary ========================================================================

# Get diary
def get_diary(username, page):
    # Films
    films = []
    data, next_page = _getData((URL_USER_DIARY) % (username, page))
    
    if data:    
        if not data.find('h2', {'class':'ui-block-heading'}):
            data = data.find('table', {'id':'diary-table'})
            data = data.find('tbody')
            data = data.findAll('tr')
        
            for film in data:
                title = film.find('span', {'class':'frame-title'}).text
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
    return films, next_page
    
    
# ============= Lists ========================================================================
    
# Get lists
def get_lists(username, page):
    # Lists
    lists = []
    data, next_page = _getData((URL_USER_LISTS) % (username, page))

    if data:
        data = data.findAll('div', {'class':'film-list-summary'})
    
        lists = [{
            'title':_getText(list, tag='h2'),
            'count':_getText(list, tag='small', split=True, delimeter='&'),
            'slug':_getText(list, tag='a', attr='href', split=True, delimeter='/', index=-2)
        } for list in data]
    
    # Return
    return lists, next_page
   
   
# Get list
def get_list(username, slug, page):
    # Films
    films = []
    url = (URL_USER_WATCHLIST) % (username, page) if slug == 'watchlist' else (URL_USER_LIST) % (username, slug, page)
    data, next_page = _getData(url)

    if data:
        data = data.findAll('li', {'class':re.compile(r'\poster-container\b')})
                
        films = [{
            'title':re.sub(r'\((.+)\)', ' ', _getText(film, tag='a', cls={'class':'frame'}, attr='title')).strip(),
            'year':_getText(film, tag='a', cls={'class':'frame'}, attr='title', match=r'\(([0-9]{4})\)'),
            'poster':_getText(film, tag='img', attr='src'),
            'pos':_getText(film, tag='p', cls={'class':'list-number'})
        } for film in data]
    
    # Return
    return films, next_page
    

# ============= Films ========================================================================

# Get film
def get_films(genre, page):
    # Films
    films = []
    data, next_page = _getData((URL_FILMS_GENRE) % (slug))

    if data:
        data = data.findAll('li', {'class':re.compile(r'\poster-container\b')})
    
        films = [{
            'title':re.sub(r'\((.+)\)', ' ', film.find('a', {'class':'frame'})['title']).strip(),
            'year':re.search(r'\(([0-9]{4})\)', film.find('a', {'class':'frame'})['title']).group(1),
            'poster':_getText(film, tag='img', attr='src'),
            'pos':_getText(film, tag='p', cls={'class':'list-number'})
        } for film in data]
    
    # Return
    return films, next_page

    
# ============= Network ======================================================================

# Get following
def get_people(username, type, page):
    # People
    people = []

    url = URL_USER_FOLLOWING if type == "following" else URL_USER_FOLLOWERS
    data, next_page = _getData((url) % (username, page))

    if data:    
        data = data.findAll('td', {'class':'table-person'})
    
        for person in data:
            name = person.find('h3', {'class':'name-heading'}).text
            username = person.find('h3', {'class':'name-heading'}).find('a')['href'].replace('/', '')
            avatar = person.find('img')['src']

            people.append({
                'name': name,
                'username': username,
                'avatar': avatar
            })

    # Return
    return people, next_page


# ============= Helpers ======================================================================

# Get page data
def _getData(url):
    try:
        data = soup(download_page(url), convertEntities=soup.HTML_ENTITIES)
    except:
        return None, None
        raise
    else:
        return data, _getNextPage(data)
        
        
# Get pagination
def _getNextPage(soup):
    hasnext = soup.find('a', {'class': 'paginate-next'})
    
    if hasnext:
        return int(hasnext['href'].split('/')[-2])
    else:
        return None
    

# Find tag
def _getText(soup, tag, cls={}, attr=None, split=False, delimeter='', index=0, match=None):
    tag = soup.find(tag, cls)
    
    if tag:
        if attr:
            text = tag[attr]
        else:
            text = tag.text
            
        # Split
        if split:
            text = text.split(delimeter)[index]
            print text
            
        # Match
        if match:
            text = re.search(match, text).group(1) if re.search(match, text) else None
    else:
        text = None
        
    return text
