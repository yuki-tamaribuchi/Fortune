def get_track_from_spotify():
	import random
	from spotipy import Spotify
	from spotipy.oauth2 import SpotifyClientCredentials

	sp = Spotify(client_credentials_manager=SpotifyClientCredentials())

	seed_genres = sp.recommendation_genre_seeds()
	seed_genres = seed_genres["genres"]
	genre_random_index = random.randint(0, len(seed_genres))
	tracks = sp.recommendations(seed_genres=[seed_genres[genre_random_index]])
	tracks = tracks["tracks"]
	track_random_index = random.randint(0, len(tracks))
	track = tracks[track_random_index]

	artists = []
	for artist in track['artists']:
		artists.append(artist['name'])

	result = {
		'track_name': track['name'],
		'artists': artists,
		'preview_url': track['preview_url'],
		'spotify_link': track['external_urls']['spotify'],
		'id': track['id']
	}
	return result