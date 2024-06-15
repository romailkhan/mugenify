from flask import Flask
import spotipy
from flask import redirect, request, session
import os
from dotenv import load_dotenv

load_dotenv(".env")

spotipy_config = {
    "client_id": os.getenv("SPOTIFY_CLIENT_ID"),
    "client_secret": os.getenv("SPOTIFY_CLIENT_SECRET"),
    "redirect_uri": os.getenv("SPOTIFY_REDIRECT_URI"),
    "scope": "user-library-read user-read-playback-state user-modify-playback-state",
}

FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")

app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY

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
    return sp.current_user()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
