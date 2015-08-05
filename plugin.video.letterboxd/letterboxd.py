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
URL_FILMS_PARAMS    = URL_FILMS + '/ajax/%s' + URL_PAGE    

URL_META_POSTER     = URL_MAIN + '/film/%s/image-150/'


# ============= Profile ======================================================================

# Get profile
def get_profile(username):    
    # Profile
    data = _getData((URL_USER) % (username))[0]
    
    name = data.find('div', {'class':'profile-name-wrap'})
    name = name.find('h1').text
    
    stats = data.find('ul', {'class':'stats'}).findAll('strong')
    stats = [stat.text.replace(',', '') for stat in stats]
    stats = {
        'films': stats[0], 
        'this_year': stats[1], 
        'lists': stats[2], 
        'following': stats[3], 
        'followers': stats[4]
    }
    
    # Return
    return name, stats


# ============= Diary ========================================================================

# Get diary
def get_diary(username, page=1):
    # Films
    films = []
    data, next_page = _getData((URL_USER_DIARY) % (username, page))
    
    if data:
        data = data.find('table', {'id':'diary-table'})
        data = data.findAll('tr', {'class': 'diary-entry-row'})

        for film in data:
            slug    = film.find('h3', {'class':'film-title prettify'}).find('a')['href'].split('/')[-2]
            title   = film.find('h3', {'class':'film-title prettify'}).text
            year    = film.find('td', {'class':'td-released center'}).text
            date    = film.find('td', {'class':'td-day diary-day center'})
            date    = '.'.join(reversed(date.find('a')['href'].split('/')[-4:-1]))
            rating  = (int(film.find('meta', {'itemprop':'rating'})['content']) / 2)
            liked   = True if film.find('span', {'class':'has-icon icon-16 large-liked icon-liked'}) else False
            rewatch = False if film.find('td', {'class':'td-rewatch center icon-status-off'}) else True
            poster  = _get_poster(slug)

            films.append({
                'slug': slug,
                'title': title, 
                'year': year, 
                'date': date,
                'rating': rating, 
                'liked': liked, 
                'rewatch': rewatch,
                'poster': poster
            })

    # Return
    return films, next_page
    
    
# ============= Lists ========================================================================
    
# Get lists
def get_lists(username, page=1):
    # Lists
    lists = []
    data, next_page = _getData((URL_USER_LISTS) % (username, page))

    if data:
        data = data.findAll('div', {'class':'film-list-summary'})
    
        lists = [{
            'title': _getText(l, tag='h2'),
            'count': _getText(l, tag='small', split=True, delimeter='&'),
            'slug': _getText(l, tag='a', attr='href', split=True, delimeter='/', index=-2)
        } for l in data]
    
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
            'title': re.sub(r'\((.+)\)', ' ', _getText(film, tag='a', cls={'class':'frame'}, attr='title')).strip(),
            'year': _getText(film, tag='a', cls={'class':'frame'}, attr='title', match=r'\(([0-9]{4})\)'),
            'poster': _getText(film, tag='img', attr='src'),
            'pos': _getText(film, tag='p', cls={'class':'list-number'}),
            'watched': True if film.find('span', {'class':re.compile(r'\icon-watched\b')}) else False
        } for film in data]
    
    # Return
    return films, next_page
    

# ============= Films ========================================================================

# Get film
def get_films(url, page):
    # Films
    films = []
    
    data, next_page = _getData((URL_FILMS_PARAMS) % (url.replace('_', '/'), page))
    
    print (URL_FILMS_PARAMS) % (url.replace('_', '/'), page)
    
    if data:
        print data
        data = data.findAll('li', {'class': 'poster-container'})
        
        films = [{
            'title':re.sub(r'\((.+)\)', ' ', film.find('a', {'class':'frame'})['title']).strip(),
            'year':re.search(r'\(([0-9]{4})\)', film.find('a', {'class':'frame'})['title']).group(1),
            'poster':_getText(film, tag='img', attr='src'),
            'pos':_getText(film, tag='p', cls={'class':'list-number'})
        } for film in data]
        
        print films
    
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
        data = download_page(url)
        data = data.decode('utf-8')
        data = soup(data)
    except Exception as e:
        print '[Letterboxd][_getData] %s' % (e)
        return None, None
    else:
        return data, _getNextPage(data)
        
        
# Get pagination
def _getNextPage(soup):
    hasnext = soup.find('a', {'class': 'paginate-next'})
    
    if hasnext:
        return int(hasnext['href'].split('/')[-2])
    else:
        return None
    

# Get poster
def _get_poster(slug):
    try:
        data = _getData(URL_META_POSTER % (slug))
        poster = data[0].find('img')['srcset'].split(' ')[0]
    except Exception as e:
        print '[Letterboxd][_get_poster] %s' % (e)
        return None
    else:
        return poster
        

# Find tag
def _getText(soup, tag, cls={}, attr=None, split=False, delimeter='', index=0, match=None):
    tag = soup.find(tag, cls)
    
    if tag:
        text = tag[attr] if attr else tag.text
            
        # Split
        if split:
            print text, '=>',
            text = text.split(delimeter)[index]
            print text
            
        # Match
        if match:
            text = re.search(match, text).group(1) if re.search(match, text) else None
    else:
        text = None
        
    return text
