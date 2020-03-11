from flask import Blueprint, request
from flask_restful import Resource, Api

from config import db

app = Blueprint('review', __name__)
api = Api(app)

reviews_ref = db.collection('reviews')


class ReviewsController(Resource):
    def get(self):
        docs = reviews_ref.stream()
        reses = [{doc.id: doc.to_dict()} for doc in docs]
        return reses,  200


api.add_resource(ReviewsController, '/reviews')
