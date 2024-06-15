import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables from .env file
load_dotenv()
env = os.environ



# Spotify API

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=env['SPOTIFY_CLIENT_ID'],
                                               client_secret=env['SPOTIFY_CLIENT_SECRET'],
                                               redirect_uri=env['SPOTIFY_REDIRECT_URI'],
                                               scope="user-library-read user-read-recently-played user-top-read playlist-modify-private"))

def get_secret():
    return env['SECRET_KEY']

def get_auth_url():
    auth_url = sp.auth_manager.get_authorize_url()
    return auth_url

def get_access_token(code : str):
    token = sp.auth_manager.get_access_token(code=code)
    return token

def refresh_access_token():
    token = sp.auth_manager.refresh_access_token()
    return token

def get_data():
    results = sp.search(q='weezer', limit=20)
    for idx, track in enumerate(results['tracks']['items']):
        print(idx, track['name'])