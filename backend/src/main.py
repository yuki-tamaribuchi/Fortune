from fastapi import FastAPI
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

import random


sp = Spotify(client_credentials_manager=SpotifyClientCredentials())

app = FastAPI(title="Fortune")


@app.get("/tracks/recommend")
def read_fortune_track():

	data = get_track_from_spotify()
	return data

def get_track_from_spotify():
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