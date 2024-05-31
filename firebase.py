import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('.secrets/betting-challenge-check24-firebase-adminsdk-gitn6-5a9f2856fd.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

""" 

firebase = Firebase(firebaseConfig)

db = firebase.database() """