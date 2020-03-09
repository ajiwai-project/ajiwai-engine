from flask import Flask
import firebase_admin
from firebase_admin import credentials, firestore


# firebase
cred = credentials.Certificate('serviceAccount.json')
firebase_admin.initialize_app(cred)
db = firestore.client()