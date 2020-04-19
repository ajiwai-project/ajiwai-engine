from flask import Blueprint, request
from flask_restful import Resource, Api

from application.services.review_service import ReviewService

app = Blueprint('review', __name__)
api = Api(app)

class ReviewController(Resource):
    def __init__(self):
        self.review_service = ReviewService()
    
    def get(self):
        return self.review_service.get_reviews(), 200


class ReviewTrainController(Resource):
    def __init__(self):
        self.review_service = ReviewService()
    
    def post(self):
        self.review_service.train()
        return {}, 200

    
api.add_resource(ReviewController, '')
api.add_resource(ReviewTrainController, '/train')