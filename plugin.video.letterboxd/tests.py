# Imports
import letterboxd

foo = '
test = [('Refresh', 'XBMC.RunScript(special://home/scripts/showtimes/default.py,%s)' % (foo))]

print test

# Tests
#run_lists()

def run_lists():
    lists = [
        {'username':'petterhj', 'slug':'watchlist', 'page':'1'},
        {'username':'petterhj', 'slug':'get-julekalender-2013', 'page':'1'}
    ]

    for list in lists:
        print '='*50
        for film in letterboxd.get_list(**list):
            for key in film:
                print film[key], '|',
            print
