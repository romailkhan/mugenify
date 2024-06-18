import os
from dotenv import load_dotenv
import spotipy

load_dotenv(".env")

spotipy_config = {
    "client_id": os.getenv("SPOTIFY_CLIENT_ID"),
    "client_secret": os.getenv("SPOTIFY_CLIENT_SECRET"),
    "redirect_uri": os.getenv("SPOTIFY_REDIRECT_URI"),
    "scope": "user-library-read user-read-playback-state user-modify-playback-state",
}

def get_spotify_oauth():
    return spotipy.SpotifyOAuth(**spotipy_config)

def get_spotify_object(auth : str):
    return spotipy.Spotify(auth=auth)