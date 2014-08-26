# Code by Nastase Alexandru.
# Github code on https://github.com/razor2611/TheMovieClips.bundle
# Manual install documentation https://support.plex.tv/hc/en-us/articles/201187656-How-do-I-manually-install-a-channel-
# or you can install it from UnSupported AppStore plugin 
#


TITLE = 'TheMovieClips'
ART = 'art-default.jpg'
ICON = 'icon-default.png'
BASE_URL = 'https://www.themovieclips.com'
API_KEY = Prefs['token']
API_URL = 'https://www.themovieclips.com/api/trailers?token=%s&type=json' % API_KEY
IMDB_URL = 'https://www.themovieclips.com/api/trailers?token=%s&type=json' % API_KEY
IN_THEATERS = 'https://www.themovieclips.com/api/in-theaters?token=%s&type=json' % API_KEY
COMMING_SOON = 'https://www.themovieclips.com/api/upcoming?token=%s&type=json' % API_KEY
POPULAR = 'https://www.themovieclips.com/api/popular?token=%s&type=json' % API_KEY
GETGENRES = 'https://www.themovieclips.com/api/getgenres?token=%s&type=json' % API_KEY
GENRE = 'https://www.themovieclips.com/api/genre?token=%s&type=json' % API_KEY
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
		oc.add(DirectoryObject(key=Callback(MoviesMenu, url=GENRE+'&genre='+genre['alias'], title=genre['name']), title=genre['name']))
	return oc
####################################################################################################
@route('/video/themovieclips/movies', page=int)
def MoviesMenu(url, title, page=1):

	oc = ObjectContainer(title2=title, view_group='List')
	response = JSON.ObjectFromURL(url, timeout=TIMEOUT)

	for trailersCollection in response.values():
		#Log('The variable x = %s' %trailersCollection)

		if 'movie_name' in trailersCollection:
			movie_name = trailersCollection['movie_name']

		if 'movie_poster' in trailersCollection:
			movie_thumb = trailersCollection['movie_poster']

		if 'link' in trailersCollection:
			movie_url = trailersCollection['link']

		if 'movie_plot' in trailersCollection:
			movie_plot = trailersCollection['movie_plot']

		if 'alternate_ids' in trailersCollection:
			movie_imdb = trailersCollection['alternate_ids']['imdb']

		oc.add(DirectoryObject(key=Callback(MovieMenu, url=IMDB_URL+'&imdb='+movie_imdb, title=movie_name, thumb_url=movie_thumb), title=movie_name, summary=movie_plot, thumb=Resource.ContentsOfURLWithFallback(movie_thumb)))

	return oc

####################################################################################################
@route('/video/themovieclips/movies/trailer')
def MovieMenu(url, title, thumb_url, section=None):

	oc = ObjectContainer(title2=title, view_group='Posters')

	response = JSON.ObjectFromURL(url, timeout=TIMEOUT)

	for trailers in response.values():

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