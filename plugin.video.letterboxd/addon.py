from xbmcswift2 import Plugin

import letterboxd

plugin = Plugin()


@plugin.route('/')
def index():
    # Items
    items = [
        {'label': 'Diary', 'path': plugin.url_for('diary')},
        {'label': 'Watchlist', 'path': plugin.url_for('watchlist')},
        {'label': 'Lists', 'path': plugin.url_for('lists')},
        {'label': 'Network', 'path': plugin.url_for('network')},
    ]
    
    # Return
    return items
    
    
@plugin.route('/diary')
def diary():
    # Items
    items = []
    
    # Get user watchlist items
    for film in letterboxd.get_user_diary():
        items.append({
            'icon':film['poster'],
            'thumbnail':film['poster'],
            'label':'%s (%s) | %s' % (film['title'], film['year'], film['rating']),
            'path':plugin.url_for('index')
        })
    
    # Return
    return items
    
    
@plugin.route('/watchlist')
def watchlist():
    # Items
    items = []
    
    # Get user watchlist items
    for film in letterboxd.get_user_watchlist():
        items.append({
            'icon':film['poster'],
            'thumbnail':film['poster'],
            'label':'%s (%s)' % (film['title'], film['year']), 
            'path':plugin.url_for('index')
        })
    
    # Return
    return items
    
    
@plugin.route('/lists')
def lists():
    # Items
    items = []
    # Return
    return items
    

# ============= Network ======================================================================
@plugin.route('/network')
def network():
    items = [
        {'label': 'Following', 'path': plugin.url_for('network_following')},
        {'label': 'Followers', 'path': plugin.url_for('network_followers')},
    ]
    return items

    
@plugin.route('/network_following')
def network_following():
    # Items
    items = []
    
    # Get following list
    for person in letterboxd.get_user_following():
        items.append({
            'icon':person['avatar'],
            'thumbnail':person['avatar'],
            'label':'%s' % (person['name']), 
            'path':plugin.url_for('index')
        })
    
    # Return
    return items
    
    
@plugin.route('/network_followers')
def network_followers():
    # Items
    items = []
    
    # Get following list
    for person in letterboxd.get_user_following():
        items.append({
            'icon':person['avatar'],
            'thumbnail':person['avatar'],
            'label':'%s' % (person['name']), 
            'path':plugin.url_for('index')
        })
    
    # Return
    return items


# ============= Main =========================================================================
if __name__ == '__main__':
    plugin.run()
