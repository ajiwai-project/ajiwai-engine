from flask import Blueprint, request
from flask_restful import abort, Resource, Api

from config import db

app = Blueprint('brand', __name__)
api = Api(app)

brands_ref = db.collection('brands')


class brandController(Resource):
    def get(self):
        docs = brands_ref.stream()
        reses = [{doc.id: doc.to_dict()} for doc in docs]
        return reses, 200


class brandsController(Resource):
    def get(self):
        docs = brands_ref.stream()
        reses = [{doc.id: doc.to_dict()} for doc in docs]
        return reses, 200


api.add_resource(brandController, '/brand')
api.add_resource(brandsController, '/brands')
