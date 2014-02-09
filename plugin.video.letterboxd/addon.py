# Imports
from xbmcswift2 import Plugin

import letterboxd


# Plugin
plugin = Plugin()


# Index
@plugin.route('/')
@plugin.route('/profile/<username>', name='profile')
def index(username=plugin.get_setting('username')):
    # Username
    #username = ''

    # Items
    items = [
        {'label': 'Diary', 'path': plugin.url_for('diary', username=username, page='1')},
        {'label': 'Watchlist', 'path': plugin.url_for('watchlist', username=username, page='1')},
        {'label': 'Lists', 'path': plugin.url_for('lists', username=username, page='1')},
        {'label': 'Network', 'path': plugin.url_for('network', username=username)},
    ] 
    
    # Return
    return items


# Diary
@plugin.route('/diary/<username>/<page>')
def diary(username, page):
    # Items
    items = []
    
    # Get user watchlist items
    for film in letterboxd.get_user_diary(username, page):
        items.append({
            'icon':film['poster'],
            'thumbnail':film['poster'],
            'label':'%s (%s) | %s' % (film['title'], film['year'], film['rating']),
            'path':plugin.url_for('index')
        })
    
    # Return
    return items
    
    
# ============= Lists ========================================================================
    
# Watchlist
@plugin.route('/watchlist/<username>/<page>')
def watchlist(username, page):
    # Items
    items = []
    
    # Get user watchlist items
    for film in letterboxd.get_user_watchlist(username, page):
        items.append({
            'icon':film['poster'],
            'thumbnail':film['poster'],
            'label':'%s (%s)' % (film['title'], film['year']), 
            'path':plugin.url_for('index')
        })
    
    # Return
    return items
    

# Lists
@plugin.route('/lists/<username>/<page>')
def lists(username, page):
    # Items
    items = []
    
    # Get user watchlist items
    for list in letterboxd.get_lists(username, page):
        items.append({
            'icon':'',
            'thumbnail':'',
            'label':'%s (%s films)' % (list['title'], list['count']),
            'path':plugin.url_for('index')
        })
    
    # Return
    return items
    

# ============= Network ======================================================================

# Network
@plugin.route('/network/<username>')
def network(username):
    items = [
        {'label': 'Following', 'path': plugin.url_for('network_following', username=username)},
        {'label': 'Followers', 'path': plugin.url_for('network_followers', username=username)},
    ]
    return items


# Following
@plugin.route('/network_following/<username>')
def network_following(username):
    # Items
    items = []
    
    # Get following list
    for person in letterboxd.get_user_following(username):
        items.append({
            'icon':person['avatar'],
            'thumbnail':person['avatar'],
            'label':'%s' % (person['name']),
            'path':plugin.url_for('profile', username=person['username'])
        })
    
    # Return
    return items
    

# Followers    
@plugin.route('/network_followers/<username>')
def network_followers(username):
    # Items
    items = []
    
    # Get following list
    for person in letterboxd.get_user_followers(username):
        items.append({
            'icon':person['avatar'],
            'thumbnail':person['avatar'],
            'label':'%s' % (person['name']), 
            'path':plugin.url_for('diary', username=person['username'], page='1')
        })
    
    # Return
    return items


# ============= Main =========================================================================

# Main
if __name__ == '__main__':
    plugin.run()
