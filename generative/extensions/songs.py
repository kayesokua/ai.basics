import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv
load_dotenv()

def recommend_song_by_mood(mood):
    client_credentials_manager = SpotifyClientCredentials(
        client_id=os.environ.get('SPOTIFY_CLIENT_ID'),
        client_secret=os.environ.get('SPOTIFY_SECRET_KEY'))
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    results = sp.search(q=f'mood:{mood}', type='track', limit=15)
    tracks = results['tracks']['items']
    preview_songs = []
    for track in tracks:
        track_information = track['name'] + ' - ' + track['artists'][0]['name']
        preview_url = track['preview_url']
        preview_songs.append({'name': track_information, 'preview_url': preview_url})
    return preview_songs