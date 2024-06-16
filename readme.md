# Gemini Contest API

This is a RESTful API for the Gemini Contest application. It is built using Flask and managed with Poetry.

## Prerequisites
Send me your email so I can add you to the Firebase project and to Spotify API
Ask me for firebase cert file and put it in the root of the project

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/gemini-contest-api.git

2. Change into the project directory:

   ```bash
   cd gemini-contest-api

3. Install the dependencies:

   ```bash
    poetry install

4. Change into the main app directory:

   ```bash
    cd gemini-contest-api/src

5. Enter the poetry shell so you can run the flask commands:

    ```bash
    poetry shell

6. Run the application:

    ```bash
     flask run
    
7. The application should now be running on `http://127.0.0.1:5000/`



## TODO

Front End
[ ] Creating Landing Page with "Get Started" Button
[ ] Main App Screen
   [ ] Chat box with Gemini API (how do we control people will only talk about music?)
   [ ] Some form of AI work on Music Data for Cool Stats and stuff?
[ ] Onboarding - Name, Email, and button to connect to Spotify
[ ] Merge Name and Email with Data we get from Spotify User Data and Store all that into Firestore DB
[ ] User Icon with Profile, Logout, etc

CORS?
[ ] Look into CORS and how to handle it with Flask

Back End
[X] Spotify Auth
[X] Database for storing user data
[ ] Connect with Google Gemini API work with frontend peeps
[ ] Security? - Look into production env instead of dev env for flask
[ ] Checkout [Spotipy API](https://spotipy.readthedocs.io/en/2.24.0/) or [Spotify Web API](https://developer.spotify.com/documentation/web-api)and see what cool things we can do with it
[ ] Deployment look into Google Firebase Hosting options