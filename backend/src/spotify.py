import os
import base64
import aiohttp
import json
import random


async def spotify_authorization():
	SPOTIPY_CLIENT_ID = os.environ.get('SPOTIPY_CLIENT_ID')
	SPOTIPY_CLIENT_SECRET = os.environ.get('SPOTIPY_CLIENT_SECRET')

	if (SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET) is not None:
		credential = SPOTIPY_CLIENT_ID+':'+SPOTIPY_CLIENT_SECRET
		encoded_credential = base64.b64encode(bytes(credential, 'utf-8'))

		payload = {
			'grant_type':'client_credentials'
		}
		headers = {
			'Authorization': 'Basic ' + encoded_credential.decode('utf-8'),
			'Content-Type': 'application/x-www-form-urlencoded'
		}
		url = 'https://accounts.spotify.com/api/token'

		async with aiohttp.ClientSession() as client:
			response = await client.post(
				url,
				data=payload,
				headers=headers
			)
		stream = response.content
		while not stream.at_eof():
			token = await stream.read()
		return json.loads(token.decode('utf-8'))
	print('Credential error')
	return

async def get_recommend_seed_genre(headers):
	if headers:
		url = 'https://api.spotify.com/v1/recommendations/available-genre-seeds'

		async with aiohttp.ClientSession() as client:
			response = await client.get(
				url,
				headers=headers
			)
		stream = response.content
		while not stream.at_eof():
			seed_genres = await stream.read()
		seed_genres = json.loads(seed_genres.decode('utf-8'))['genres']
		seed_genre = seed_genres[random.randint(0, len(seed_genres))]
		return seed_genre
	return


async def get_recommendation_tracks(headers):
	if headers:
		seed_genre = await get_recommend_seed_genre(headers)

		if seed_genre:
			url = 'https://api.spotify.com/v1/recommendations?seed_genres={}'.format(seed_genre)
			async with aiohttp.ClientSession() as client:
				response = await client.get(
					url,
					headers = headers
				)
			stream = response.content
			while not stream.at_eof():
				tracks = await stream.read()
		return json.loads(tracks.decode('utf-8'))['tracks']
	return


async def get_track_from_spotify():
	token = await spotify_authorization()
	if token:
		headers = {
			'Authorization': 'Bearer ' + token['access_token'],
			'Content-Type': 'application/json'
		}
		tracks = await get_recommendation_tracks(headers)
		if tracks:
			track = tracks[random.randint(0, len(tracks))]

			artists = []
			for artist in track['artists']:
				artists.append(artist['name'])

			track = {
				'track_name': track['name'],
				'artists': artists,
				'preview_url': track['preview_url'],
				'spotify_link': track['external_urls']['spotify'],
				'id': track['id']
			}
			return track
	return None


		

'''
import asyncio
loop = asyncio.new_event_loop()
track = loop.run_until_complete(get_track_from_spotify())
print(track)
'''


#async def get_track_from_spotify():
#	import random
#	from spotipy import Spotify
#	from spotipy.oauth2 import SpotifyClientCredentials
#
#	sp = Spotify(client_credentials_manager=SpotifyClientCredentials())
#
#	seed_genres = sp.recommendation_genre_seeds()
#	seed_genres = seed_genres["genres"]
#	genre_random_index = random.randint(0, len(seed_genres))
#	tracks = sp.recommendations(seed_genres=[seed_genres[genre_random_index]])
#	tracks = tracks["tracks"]
#	track_random_index = random.randint(0, len(tracks))
#	track = tracks[track_random_index]
#
#	artists = []
#	for artist in track['artists']:
#		artists.append(artist['name'])
#
#	result = {
#		'track_name': track['name'],
#		'artists': artists,
#		'preview_url': track['preview_url'],
#		'spotify_link': track['external_urls']['spotify'],
#		'id': track['id']
#	}
#	return result