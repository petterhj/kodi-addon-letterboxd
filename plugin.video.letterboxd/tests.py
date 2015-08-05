# # Imports
# import letterboxd as lb

# print '='*20

# for film in lb.get_diary('petterhj')[0]:
#    print film

# # print lb.get_profile('petterhj')
# # print lb._get_poster('the-guest-2014')

# print '='*20

# import resources.models.film

from xbmcswift2 import xbmc, xbmcgui, Plugin

xbmc.executebuiltin("Notification('Title','Message')")

plugin = Plugin()

films = plugin.get_storage('films')

def test():
	print 'test ran'
	return '2014'


# f1 = {'slug': 'hateship-loveship', 'title': 'Hateship, loveship', 'year': test()}
# f2 = {'slug': 'the-matrix', 'title': 'The Matrix', 'year': '1999'}

# films[f1['slug']] = f1

# print films['hateship-loveship']

# films.sync()

print films.items()
