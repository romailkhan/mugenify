import os
from dotenv import load_dotenv
from flask import Flask
from flask import redirect, request, session, jsonify
from flask_session import Session
from flask_cors import CORS
from db.db import get_user_collection
from utils import utils


load_dotenv(".env")

FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")

app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY
CORS(app, supports_credentials=True)

app.config["SESSION_TYPE"] = "filesystem"
Session(app)

sp_oauth = utils.get_spotify_oauth()


@app.route("/")
def home():
    if session.get("user", None):
        return f"<p>Hello, {session['user']['display_name']}!</p>"
    return "<p>Hello, World!</p>"


@app.route('/login', methods=['GET'])
def login():
    print("reached login")
    auth_url = sp_oauth.get_authorize_url()
    session["token_info"] = sp_oauth.get_cached_token()
    return {'auth_url': auth_url}


@app.route('/callback', methods=['GET'])
def callback():
    print("reached callback")
    token_info = sp_oauth.get_access_token(request.args["code"])
    session["token_info"] = token_info
    return redirect("/add_user_to_db")


@app.route("/add_user_to_db")
def add_user_to_db():
    print("reached db")
    token_info = session.get("token_info", None)
    if not token_info:
        return redirect("/login")
    sp = utils.get_spotify_object(token_info["access_token"])
    
    # add user to firestore
    user = sp.current_user()
    user_id = user["id"]
    get_user_collection().document(user_id).set(user)
    
    # add user to session
    session["user"] = user
    
    return redirect('http://localhost:5001/app')

# send session data to frontend
@app.route("/session", methods=["GET"])
def get_session():
    print("reached session")
    return (session["user"], 200)
    
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
