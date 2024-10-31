import os
from dotenv import load_dotenv
from flask import Flask, redirect, request, session, jsonify
from flask_session import Session
from flask_cors import CORS
from db.db import get_user_collection
from utils import utils
from datetime import timedelta
import uuid
import datetime
import google.generativeai as genai


load_dotenv(".env")

FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY
CORS(app, supports_credentials=True, resources={
    r"/*": {
        "origins": ["http://localhost:5001"],  # Your frontend URL
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": True
    }
})

app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config.update(
    SESSION_COOKIE_SAMESITE="None",
    SESSION_COOKIE_SECURE=True,
    PERMANENT_SESSION_LIFETIME=timedelta(days=1),
)

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
    
    print(session["user"])
    
    return redirect('http://localhost:5001/app')

# send session data to frontend
@app.route("/session", methods=["GET"])
def get_session():
    print("reached session")
    user = session.get("user", None)
    
    print(session["user"])
    
    if user is None:
        return jsonify({"error": "No user in session"}), 404
    else:
        return jsonify(user), 200



@app.route("/gemini", methods=["POST"])
def gemini():
    # Get theme from request JSON
    data = request.get_json()
    theme = data.get('theme', '')
    
    if not theme:
        return jsonify({"error": "No theme provided"}), 400

    try:
        model = genai.GenerativeModel("gemini-1.0-pro")
        prompt = model.generate_content(
            f"You are a music recommendation bot. Generate exactly 5 popular song titles that match the theme: '{theme}'. "
            "Format your response as a simple numbered list with just the song names. "
            "Example format:\n1. Song Name 1\n2. Song Name 2\n etc."
        )
        
        # Ensure we have a response
        if not prompt.text:
            return jsonify({"error": "No response from AI model"}), 500

        # Create a timestamp and unique ID for the playlist
        now = datetime.datetime.now()
        uuid_str = str(uuid.uuid4())
        
        response = {
            "uuid": uuid_str,
            "theme": theme,
            "songs": prompt.text.strip().split('\n'),  # Convert to list of songs
            "time": now.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return jsonify({"error": "Failed to generate playlist"}), 500

@app.route("/storeplaylist", methods=["POST"])
def store_playlist():
    try:
        # Get playlist data from request
        playlist_data = request.get_json()
        
        # Validate required fields
        required_fields = ['uuid', 'theme', 'songs', 'time']
        if not all(field in playlist_data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
            
        # Get current user from session
        user = session.get("user")
        if not user:
            print("No user in session")  # Debug print
            return jsonify({"error": "User not authenticated"}), 401
            
        try:
            # Create playlist document in Firestore
            playlist_doc = {
                "uuid": playlist_data["uuid"],
                "theme": playlist_data["theme"],
                "songs": playlist_data["songs"],
                "time": playlist_data["time"],
                "user_id": user["id"],
                "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Store in Firestore
            user_doc_ref = get_user_collection().document(user["id"])
            user_doc_ref.collection("playlists").document(playlist_data["uuid"]).set(playlist_doc)
            
            return jsonify({
                "message": "Playlist stored successfully",
                "playlist": playlist_doc
            }), 200
            
        except Exception as e:
            print(f"Firestore error: {str(e)}")  # Debug print
            return jsonify({"error": "Database error"}), 500
            
    except Exception as e:
        print(f"General error: {str(e)}")  # Debug print
        return jsonify({"error": "Failed to store playlist"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)