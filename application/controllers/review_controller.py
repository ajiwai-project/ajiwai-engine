from flask import Blueprint, request
from flask_restful import Resource, Api

from application.services.review_service import ReviewService

app = Blueprint('review', __name__)
api = Api(app)


class ReviewController(Resource):
    def __init__(self):
        self.reivew_service = ReviewService()

    def get(self):
        self.reivew_service.train()
        return {}, 200


api.add_resource(ReviewController, '/train')