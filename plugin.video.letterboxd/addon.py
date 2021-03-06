# Imports
from datetime import date

from xbmcswift2 import xbmc, xbmcgui, Plugin

import context_menus
import letterboxd
import database


# Database
database = Database()

# Plugin
plugin = Plugin()


# ============= Profile ======================================================================

# Index
@plugin.route('/')
@plugin.route('/profile/<username>', name='profile')
def index(username=plugin.get_setting('username')):
    # Settings
    if not username:
        plugin.open_settings()
        username = plugin.get_setting('username')
    
    # Profile
    name, stats = letterboxd.get_profile(username)
    current = True if username == plugin.get_setting('username') else False
    
    # Items
    items = [
        {'label': 'Diary', 'context_menu': context_menus.list(), 'path': plugin.url_for('diary', username=username, page='1')},
        {'label': 'Watchlist', 'path': plugin.url_for('list', username=username, slug='watchlist', page='1')},
        {'label': 'Lists (%s lists)' % (stats['lists']), 'path': plugin.url_for('lists', username=username, page='1')},
        {'label': 'Network', 'path': plugin.url_for('network', username=username, following=stats['following'], followers=stats['followers'])},
        #{'label': 'Test', 'path': plugin.url_for('test')},    
    ]

    for item in items:
        item['context_menu'] = context_menus.list()
        item['replace_context_menu'] = True

        item['label'] = name + '\'s ' + item['label'] if not current else item['label']
    
    # Discover
    if current:
        items.append({'label': 'Discover', 'path': plugin.url_for('discover')})
    
    # Return
    return items
    
    
# ============= Diary ========================================================================

# Diary
@plugin.route('/diary/<username>/<page>')
def diary(username, page):
    # Content type
    plugin.set_content('movies')
    
    # Items
    films, next_page = letterboxd.get_diary(username, page)
    
    items = [{
        'icon':film['poster'],
        'thumbnail':film['poster'],
        'label':'%s (%s)' % (film['title'], film['year']),
        'info': {
            'genre': 'Date: %s | Rating: %s | Liked: %s | Rewatch: %s' % (film['date'], film['rating'], film['liked'], film['rewatch']),
            'rating': (float(film['rating']) * 2)
        },
        'context_menu': context_menus.film(film['title']),
        'replace_context_menu': True,
        'path':plugin.url_for('index')
    } for film in films]
    
    # Pagination
    items = _pagination(items, page, next_page, route='diary', options={'username':username})
    
    # Return
    return items
    
    
# ============= Lists ========================================================================

# Lists
@plugin.route('/lists/<username>/<page>')
def lists(username, page):
    # Items
    lists, next_page = letterboxd.get_lists(username, page)
    
    items = [{
        'icon': '',
        'thumbnail': '',
        'label': '%s (%s)' % (list['title'], list['count']),
        'path': plugin.url_for('list', username=username, slug=list['slug'], page=1)
    } for list in lists]
    
    # Pagination
    items = _pagination(items, page, next_page, route='lists', options={'username':username})
    
    # Return
    return items

    
# List
@plugin.route('/list/<username>/<slug>/<page>')
def list(username, slug, page):
    # Content type
    plugin.set_content('movies')
    
    # Items
    label = '%s (%s)'
    label_ranked = '[COLOR yellow]%s.[/COLOR] ' + label
    
    films, next_page = letterboxd.get_list(username, slug, page)
    
    items = [{
        'icon': film['poster'],
        'thumbnail': film['poster'],
        'label': label_ranked % (film['pos'], film['title'], film['year']) if film['pos'] else label % (film['title'], film['year']),
        'info': {
            'genre': 'test, foo, bar',
            'playcount': 1 if film['watched'] else 0
        },
        'context_menu': context_menus.film(film['title']),
        'replace_context_menu': True,
        'path': plugin.url_for('index')
    } for film in films]
    
    # Pagination
    items = _pagination(items, page, next_page, route='list', options={'username':username, 'slug':slug})
    
    # Return
    return plugin.finish(items, update_listing=True)
    

# ============= Network ======================================================================

# Network
@plugin.route('/network/<username>')
def network(username):
    # Items
    items = [
        {'label': 'Following (%s people)' % (plugin.request.args['following'][0]), 'path': plugin.url_for('people', username=username, type='following', page='1')},
        {'label': 'Followers (%s people)' % (plugin.request.args['followers'][0]), 'path': plugin.url_for('people', username=username, type='followers', page='1')},
    ]
    
    # Return
    return items


# People
@plugin.route('/people/<username>/<type>/<page>')
def people(username, type, page):
    # Items
    people, next_page = letterboxd.get_people(username, type, page)
    
    items = [{
        'icon':person['avatar'],
        'thumbnail':person['avatar'],
        'label':'%s' % (person['name']),
        'path':plugin.url_for('profile', username=person['username'])
    } for person in people]
    
    # Pagination
    items = _pagination(items, page, next_page, route='people', options={'username':username, 'type': type})
    
    # Return
    return items


# ============= Films =====================================================================

# Discover
@plugin.route('/discover')
def discover():
    # Items
    items = [
        {'label': 'Films by popularity', 'path': plugin.url_for('filter')},
        {'label': 'Films by rating', 'path': plugin.url_for('filter')},  
        {'label': 'Popular with friends', 'path': plugin.url_for('index')},  
        {'label': 'Just reviewed', 'path': plugin.url_for('index')},
        {'label': 'Popular reviews this week', 'path': plugin.url_for('index')},
        {'label': 'Popular reviewers', 'path': plugin.url_for('index')},
        {'label': 'Crew picks', 'path': plugin.url_for('index')},
    ] 
    
    # Return
    return items


# Filter
@plugin.route('/filter')
def filter():
    # Items
    items = [
        {'label': 'By genre', 'path': plugin.url_for('index')},
        {'label': 'By decade', 'path': plugin.url_for('index')},
        {'label': 'By year', 'path': plugin.url_for('years')},
    ] 
    
    # Return
    return items


# Year
@plugin.route('/years')
def years():
    # Return
    return [{
        'label': '%s' % (year), 
        'path': plugin.url_for('index')
    } for year in reversed(range(1880, (date.today().year+1)))]
    
    
# Decade
@plugin.route('/decades')
def decades():
    # Return
    return [{
        'label': '%s' % (decade),
        'path': plugin.url_for('index')
    } for decade in reversed(range(1880, (date.today().year+1))[0::10])]
    
    
# Genres
@plugin.route('/genres')
def genres():
    # Genres
    genres = [
        'Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Eastern', 
        'Family', 'Fantasy', 'Film Noir', 'Foreign', 'History', 'Horror', 'Indie', 'Music', 'Musical', 
        'Mystery', 'Romance', 'Science Fiction', 'Short', 'Sports', 'Thriller', 'War', 'Western'
    ]
    
    # Items
    items = [{'label':'%s' % (genre), 'path':plugin.url_for('films', url='genre_' + genre.lower().replace(' ', '-'), page=1)} for genre in genres]

    # Return
    return items
	

# Films
@plugin.route('/films/<url>/<page>')
def films(url, page):
    # Content type
    plugin.set_content('movies')
    
    # Items
    films, next_page = letterboxd.get_films(url, page)
    
    items = [{
        'icon': film['poster'],
        'thumbnail': film['poster'],
        'label': '%s (%s)' % (film['title'], film['year']),
        'info': {
            'genre': 'test, foo, bar'
        },
        'context_menu': context_menus.film(film['title']),
        'replace_context_menu': True,
        'path': plugin.url_for('index')
    } for film in films]
    
    # Pagination
    items = _pagination(items, page, next_page, route='films', options={'url':url})
    
    # Return
    return plugin.finish(items, update_listing=True)


# Pagination
def _pagination(items, page, next_page, route, options):
    # Next/Prev
    if next_page:
        options['page'] = str(next_page)
    
        items.append({
            'label': 'Next page >>',
            'path': plugin.url_for(route, **options)
        })
        
    if int(page) > 1:
        options['page'] = str((int(page) - 1))
        
        items.insert(0, {
            'label': '<< Previous page',
            'path': plugin.url_for(route, **options)
        })
    
    # Return
    return items
    
    
# ============= Main =========================================================================

# Main
if __name__ == '__main__':
    plugin.run()
