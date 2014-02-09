from xbmcswift2 import Plugin

import letterboxd

plugin = Plugin()


@plugin.route('/')
def index():
    items = [
        {'label': 'Diary', 'path': plugin.url_for('diary')},
        {'label': 'Watchlist', 'path': plugin.url_for('watchlist')},
        {'label': 'Lists', 'path': plugin.url_for('lists')},
    ]
    return items
    
    
@plugin.route('/diary')
def diary():
    # Items
    items = []
    
    # Get user watchlist items
    for film in letterboxd.get_user_diary():
        items.append({
            'icon':'http://skyfall.cf.letterboxd.com/resized/film-poster/4/1/8/5/3/41853-torsk-pa-tallinn-0-35-0-50-crop.jpg?k=9a1db22f09',
            'label': '%s (%s) | %s' % (film['title'], film['year'], film['rating']), 
            'path': plugin.url_for('index')
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
            'thumbnail':'http://skyfall.cf.letterboxd.com/resized/film-poster/4/1/8/5/3/41853-torsk-pa-tallinn-0-35-0-50-crop.jpg?k=9a1db22f09',
            'label': '%s (%s)' % (film['title'], film['year']), 
            'path': plugin.url_for('index')
        })
    
    # Return
    return items
    
    
@plugin.route('/lists')
def lists():
    items = []
    return items
    
    
@plugin.route('/film/<id>')
def film(id):
    items = []
    return items



if __name__ == '__main__':
    plugin.run()
