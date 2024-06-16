import firebase_admin
from firebase_admin import credentials, firestore


cred = credentials.Certificate("../firebase-cert.json")
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

def get_user_collection():
    return db.collection("users")