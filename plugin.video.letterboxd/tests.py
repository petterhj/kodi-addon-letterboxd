# Imports
import letterboxd

def run_diaries():
    diaries = [
        {'username':'petterhj', 'page':'1'},
        #{'username':'petterhj', 'slug':'get-julekalender-2013', 'page':'1'}
    ]
    
    for diary in diaries:
        print '='*50
        for film in letterboxd.get_diary(**diary):
            for key in film:
                print film[key], '|',
            print

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

            
# Tests
#run_lists()
run_diaries()