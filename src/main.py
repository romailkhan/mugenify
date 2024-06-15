from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
import util.util as util

app = FastAPI()

session = {}

@app.get("/")
def home():
    return {"Hello": "World"}

@app.get("/login")
def login():
    auth_url = util.get_auth_url()
    session['auth_url'] = auth_url
    print(f"\nauth_url: {auth_url}")

@app.get("/callback")
def callback(code: str):
    token = util.get_access_token(code)
    session['token'] = token
    print(f"\ntoken: {token}")

# @app.get("/app")
# def app():
#     if 'token' not in session:
#         return RedirectResponse(url='/login')
#     else:
#         return {"App": "Spotify"}

# print session
@app.get("/session")
def get_session():
    return session