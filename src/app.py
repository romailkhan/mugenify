import os
from dotenv import load_dotenv
import spotipy
from flask import Flask
from flask import redirect, request, session
from db.db import get_user_collection
from utils import utils
import uuid6
import datetime



load_dotenv(".env")

FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")

app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY

spotipy_config = {
    "client_id": os.getenv("SPOTIFY_CLIENT_ID"),
    "client_secret": os.getenv("SPOTIFY_CLIENT_SECRET"),
    "redirect_uri": os.getenv("SPOTIFY_REDIRECT_URI"),
    "scope": "user-library-read user-read-playback-state user-modify-playback-state",
}

sp_oauth = spotipy.SpotifyOAuth(**spotipy_config)


@app.route("/")
def home():
    if session.get("user", None):
        return f"<p>Hello, {session['user']['display_name']}!</p>"
    return "<p>Hello, World!</p>"


@app.route("/login")
def login():
    auth_url = sp_oauth.get_authorize_url()
    session["token_info"] = sp_oauth.get_cached_token()
    return redirect(auth_url)


@app.route("/callback")
def callback():
    token_info = sp_oauth.get_access_token(request.args["code"])
    session["token_info"] = token_info
    return redirect("/add_user_to_db")


@app.route("/add_user_to_db")
def add_user_to_db():
    token_info = session.get("token_info", None)
    if not token_info:
        return redirect("/login")
    sp = spotipy.Spotify(auth=token_info["access_token"])
    
    # add user to firestore
    user = sp.current_user()
    user_id = user["id"]
    get_user_collection().document(user_id).set(user)
    
    # add user to session
    session["user"] = user

    return redirect("/")

@app.route("/gemini")
def gemini():
    user_id = session["user"]["id"]
    prompt = "Happy"
    num = 5
    response = utils.gemini_api(prompt, num)
    now = datetime.datetime.now()

    uuid = str(uuid6.uuid6())
    playlist = {
        "uuid": uuid,
        "prompt": prompt,
        "songs": response,
        "time": now
    }
    user_collection = get_user_collection()
    user_collection.document(user_id).collection("playlists").add(playlist)

    playlists_ref = user_collection.document(user_id).collection("playlists")
    playlists = playlists_ref.stream()  # Retrieve all playlist documents

    for playlist in playlists:
        print(f"Playlist ID: {playlist.id}, Data: {playlist.to_dict()}")
    
    return(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
