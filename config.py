from flask import Flask
import firebase_admin
from firebase_admin import credentials, firestore
import json


# firebase
cred = credentials.Certificate('serviceAccount.json')
firebase_admin.initialize_app(cred)
firestore_db = firestore.client()
memory_reviews_json = open('model/assets/reviews_dump.json', 'r')
memory_reviews_db = json.load(memory_reviews_json)