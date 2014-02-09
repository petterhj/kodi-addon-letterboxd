# Imports
from xbmcswift2 import Plugin

import letterboxd


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
    
    # Items
    items = [
        {'label': 'Diary', 'path': plugin.url_for('diary', username=username, page='1')},
        {'label': 'Watchlist', 'path': plugin.url_for('list', username=username, slug='watchlist', page='1')},
        {'label': 'Lists', 'path': plugin.url_for('lists', username=username, page='1')},
        {'label': 'Network', 'path': plugin.url_for('network', username=username)},
    ] 
    
    # Return
    return items


# Diary
@plugin.route('/diary/<username>/<page>')
def diary(username, page):
    # Items
    items = [{
        'icon':film['poster'],
        'thumbnail':film['poster'],
        'label':'%s (%s) | %s' % (film['title'], film['year'], film['rating']),
        'path':plugin.url_for('index')
    } for film in letterboxd.get_diary(username, page)]
    
    # Return
    return items
    
    
# ============= Lists ========================================================================

# Lists
@plugin.route('/lists/<username>/<page>')
def lists(username, page):
    # Items
    items = [{
        'icon':'',
        'thumbnail':'',
        'label':'%s (%s films)' % (list['title'], list['count']),
        'path':plugin.url_for('list', username=username, slug=list['slug'], page=1)
    } for list in letterboxd.get_lists(username, page)]
    
    # Return
    return items

    
# List
@plugin.route('/list/<username>/<slug>/<page>')
def list(username, slug, page):
    # Items
    items = [{
        'icon':film['poster'],
        'thumbnail':film['poster'],
        'label':'%s. %s (%s)' % (film['pos'], film['title'], film['year']) if film['pos'] else '%s (%s)' % (film['title'], film['year']),
        'path':plugin.url_for('index')
    } for film in letterboxd.get_list(username, slug, page)]
    
    # Return
    return items
    

# ============= Network ======================================================================

# Network
@plugin.route('/network/<username>')
def network(username):
    # Items
    items = [
        {'label': 'Following', 'path': plugin.url_for('people', username=username, type="following")},
        {'label': 'Followers', 'path': plugin.url_for('people', username=username, type="followers")},
    ]
    
    # Return
    return items


# People
@plugin.route('/people/<username>/<type>')
def people(username, type):
    # Items
    people = letterboxd.get_following(username) if type == 'following' else letterboxd.get_followers(username)
    
    items = [{
        'icon':person['avatar'],
        'thumbnail':person['avatar'],
        'label':'%s' % (person['name']),
        'path':plugin.url_for('profile', username=person['username'])
    } for person in people]
    
    # Return
    return items


# ============= Main =========================================================================

# Main
if __name__ == '__main__':
    plugin.run()
