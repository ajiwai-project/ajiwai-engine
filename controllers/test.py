from flask import Blueprint, request
from flask_restful import Resource, Api

app = Blueprint('test', __name__)
api = Api(app)


class TestController(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(TestController, '/test')
