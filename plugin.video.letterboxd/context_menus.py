# Context menus
def list():
    # Menu
    menu = [
        ('Refresh', 'XBMC.RunScript(special://home/scripts/showtimes/default.py,Iron Man)')
    ]
    
    # Return
    return menu
    

def film(movie_title):
    # Menu
    menu = [
        ('Search Trailer on YouTube', 'XBMC.Container.Update(plugin://plugin.video.youtube/?path=/root/search&feed=search&search=%s+Trailer)' % movie_title)
    ]
    
    # Return
    return menu