from flask import Blueprint, request, jsonify
from flask_restful import abort, Resource, Api
import sys
from pprint import pprint

from config import db
from infrastructure.repositories.brand_repository import BrandRepository
from infrastructure.dao.brand_dao import BrandDao
from application.services.brand_service import BrandService

app = Blueprint('brand', __name__)
api = Api(app)


class brandController(Resource):

    def __init__(self):
        self.brand_repository = BrandRepository()
        self.brand_dao = BrandDao()

    def get(self, brand_id):
        res = self.brand_dao.find_by_brand_id(brand_id)
        return res, 200


class brandsController(Resource):

    def __init__(self):
        self.brand_dao = BrandDao()

    def get(self):
        docs = self.brand_dao.find_all()
        reses = [{doc.id: doc.to_dict()} for doc in docs]
        return reses, 200

class brandPredictController(Resource):
    def __init__(self):
        self.brand_service = BrandService()


    def post(self):
        body = request.get_json(force=True)
        res = self.brand_service.predict(body['sentence'])
        return res, 200


api.add_resource(brandController, '/<string:brand_id>')
api.add_resource(brandPredictController, '/predict')
api.add_resource(brandsController, '')
