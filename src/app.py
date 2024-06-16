import os
from dotenv import load_dotenv
import spotipy
from flask import Flask
from flask import redirect, request, session
from db.db import get_user_collection



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
def hello_world():
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
    return redirect("/app")


@app.route("/app")
def main_app():
    token_info = session.get("token_info", None)
    if not token_info:
        return redirect("/login")
    sp = spotipy.Spotify(auth=token_info["access_token"])
    
    # add user to firestore
    user = sp.current_user()
    user_id = user["id"]
    get_user_collection().document(user_id).set(user)

    return user

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
