# Imports
import letterboxd
import requests


#id=username
#id=password

#response = requests.post('http://letterboxd.com/user/login.do', data={'username': 'petterhj', 'password': 'fjxa694p'})

#print response.text

import mechanize

br = mechanize.Browser()
br.open('http://www.letterboxd.com')
print br.title()
#print br.select_form(predicate=lambda f: 'id' in f.attrs and f.attrs['id'] == 'signin')
#print br.select_form(nr=1)
#br['username'] = 'petterhj'
#br['password'] = 'fjxa694p'
#response = br.submit()
#print br.title()
#print response

br.form = list(br.forms())[0] 
br['username'] = 'petterhj'
br['password'] = 'fjxa694p'
response = br.submit()

print response.read()

'''
form = [f for f in br.forms()][0]
form['username'] = 'petterhj'
form['password'] = 'fjxa694p'
response = form.click()
br.open(response)
print br.title()
print br.read()
#print br.submit()
'''

'''
def run_films():
    genres = [
        {'genre':'action', 'page':'1'},
        #{'username':'petterhj', 'slug':'get-julekalender-2013', 'page':'1'}
    ]
    
    for genre in genres:
        print '='*50
        for film in letterboxd.get_films(**diary):
            for key in film:
                print film[key], '|',
            print
            

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
#run_films()

print letterboxd.get_list('petterhj', 'collection', '2')
'''