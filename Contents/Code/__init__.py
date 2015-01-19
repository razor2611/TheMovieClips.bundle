# Code by Nastase Alexandru.
# Version 1.2.1
# Github code on https://github.com/razor2611/TheMovieClips.bundle
# Manual install documentation https://support.plex.tv/hc/en-us/articles/201187656-How-do-I-manually-install-a-channel-
# or you can install it from UnSupported AppStore plugin 
#


TITLE = 'TheMovieClips'
ART = 'art-default.jpg'
ICON = 'icon-default.png'
BASE_URL = 'https://www.themovieclips.com'
API_KEY = Prefs['token']
API_URL = 'https://www.themovieclips.com/api/v1/trailers?token=%s&type=json' % API_KEY
IMDB_URL = 'https://www.themovieclips.com/api/v1/trailers?token=%s&type=json' % API_KEY
IN_THEATERS = 'https://www.themovieclips.com/api/v1/in-theaters?token=%s&type=json' % API_KEY
COMMING_SOON = 'https://www.themovieclips.com/api/v1/upcoming?token=%s&type=json' % API_KEY
POPULAR = 'https://www.themovieclips.com/api/v1/popular?token=%s&type=json' % API_KEY
GETGENRES = 'https://www.themovieclips.com/api/v1/getgenres?token=%s&type=json' % API_KEY
GENRE = 'https://www.themovieclips.com/api/v1/genre?token=%s&type=json' % API_KEY
RESOLUTIONS = ['360p', '480p', '720p', '1080p']
TIMEOUT = 100000;

####################################################################################################
def Start():

	Plugin.AddViewGroup('InfoList', viewMode='InfoList', mediaType='items')
	Plugin.AddViewGroup('List', viewMode='List', mediaType='items')
	Plugin.AddViewGroup('Posters', viewMode='List', mediaType='items')

	ObjectContainer.title1 = TITLE
	ObjectContainer.art = R(ART)
	DirectoryObject.thumb = R(ICON)
	HTTP.CacheTime = CACHE_1HOUR
	HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:20.0) Gecko/20100101 Firefox/20.0'

####################################################################################################
@handler('/video/themovieclips', TITLE)
def MainMenu():

	oc = ObjectContainer(view_group='List')
	oc.add(PrefsObject(title="Settings"))
	oc.add(DirectoryObject(key=Callback(MoviesMenu, url=API_URL+'&limit=30', title='Latest'), title='Latest Trailers'))
	oc.add(DirectoryObject(key=Callback(MoviesMenu, url=IN_THEATERS, title='In Theathers'), title='In Theathers'))
	oc.add(DirectoryObject(key=Callback(MoviesMenu, url=COMMING_SOON, title='Trailers Comming Soon'), title='Comming Soon'))
	oc.add(DirectoryObject(key=Callback(MoviesMenu, url=POPULAR, title='Popular Trailers'), title='Popular Trailers'))
	oc.add(DirectoryObject(key=Callback(GenresMenu, url=GETGENRES, title='Genres'), title='Genres'))
	return oc
####################################################################################################
@route('/video/themovieclips/genres')
def GenresMenu(url, title):


	oc = ObjectContainer(title2=title, view_group='List')
	response = JSON.ObjectFromURL(url, timeout=TIMEOUT)
	for genre in response.values():
		oc.add(DirectoryObject(
			key = Callback(MoviesMenu, url=GENRE+'&genre='+genre['alias'], title=genre['name']),
			title = genre['name']
		))

	oc.objects.sort(key = lambda obj: obj.title)
	return oc
####################################################################################################
@route('/video/themovieclips/movies', page=int)
def MoviesMenu(url, title, page=1):

	oc = ObjectContainer(title2=title, view_group='List')

	trailers = BuildDict(url)
	for trailer in trailers:
		oc.add(DirectoryObject(key=Callback(MovieMenu, url=IMDB_URL+'&imdb='+trailer['item_imdb'], title=trailer['item_title'], thumb_url=trailer['item_poster']), title=trailer['item_movie_title'], summary=trailer['item_summary'], thumb=Resource.ContentsOfURLWithFallback(trailer['item_poster'])))

	return oc

####################################################################################################
@route('/video/themovieclips/movies/trailer')
def MovieMenu(url, title, thumb_url, section=None):

	oc = ObjectContainer(title2=unicode(title), view_group='Posters')

	response = JSON.ObjectFromURL(url, timeout=TIMEOUT)

#	for trailers in response.values():
	for trailers in response:

		if 'name' in trailers:
			name = trailers['name']

		if 'thumbs' in trailers:
			movie_thumb = trailers['thumbs']['small']

		if 'movie_plot' in trailers:
			movie_plot = trailers['movie_plot']

		if 'link' in trailers:
			movie_link = trailers['link']

		movie = URLService.MetadataObjectForURL(trailers['link'])
		oc.add(movie)

	return oc

########################################################################################################
def BuildDict(url):

	trailers = []
     
	response = JSON.ObjectFromURL(url, timeout=TIMEOUT)

#	for key in response.keys():
	for results in response:
#		results = response[key]

		if 'id' in results:
			id = results['id']
		if 'title' in results:
			title = results['title']
		if 'title' in results['movie']:
			movie_name = results['movie']['title']
		if 'plot' in results['movie']:
			movie_plot = results['movie']['plot']
		if 'posters' in results['movie']:
			movie_poster = results['movie']['posters']
		if 'thumb' in results:
			movie_thumb = results['thumb']['small']
		if 'imdb_id' in results:
			movie_imdb = results['imdb_id']


		trailer = {
#			'id': key,
			'id': id,
			'item_title': title,
			'item_movie_title': movie_name,			
			'item_summary': movie_plot,
			'item_thumb': movie_thumb,
			'item_poster': movie_poster, 
			'item_imdb': movie_imdb
		}
		trailers.append(trailer)

	trailers.sort(key=lambda x: int(x['id']))

	return trailers