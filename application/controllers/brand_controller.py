from flask import Blueprint, request
from flask_restful import abort, Resource, Api
import sys

from config import db
from infrastructure.repositories.brand_repository import BrandRepository
from infrastructure.dao.brand_dao import BrandDao

app = Blueprint('brand', __name__)
api = Api(app)

brands_ref = db.collection('brands')


class brandController(Resource):

    def __init__(self):
        self.brand_repository = BrandRepository()
        self.brand_dao = BrandDao()

    def get(self):
        brand_id = request.args.get('brand_id')
        res = self.brand_dao.find_by_brand_id(brand_id)
        return res, 200


class brandsController(Resource):

    def __init__(self):
        self.brand_dao = BrandDao()

    def get(self):
        docs = self.brand_dao.find_all()
        reses = [{doc.id: doc.to_dict()} for doc in docs]
        return reses, 200


api.add_resource(brandController, '/brand')
api.add_resource(brandsController, '/brands')
