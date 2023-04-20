import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv
load_dotenv()

def get_preview_songs_by_mood(mood):
    """
    Get 5 previews of songs based on a given mood.
    """

    # Authenticate with the Spotify API
    client_credentials_manager = SpotifyClientCredentials(
        client_id=os.environ.get('SPOTIFY_CLIENT_ID'),
        client_secret=os.environ.get('SPOTIFY_SECRET_KEY'))
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Search for tracks with the given mood
    results = sp.search(q=f'mood:{mood}', type='track', limit=15)

    # Extract the track information for the preview songs
    tracks = results['tracks']['items']
    preview_songs = []
    for track in tracks:
        track_information = track['name'] + ' - ' + track['artists'][0]['name']
        preview_url = track['preview_url']
        preview_songs.append({'name': track_information, 'preview_url': preview_url})

    # Return the track information for the preview songs
    return preview_songs
