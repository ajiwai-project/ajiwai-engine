from flask import Blueprint, request
from flask_restful import abort, Resource, Api

from application import db

app = Blueprint('sake', __name__)
api = Api(app)

sakes_ref = db.collection('users')
SAKES = {}


def abort_if_todo_doesnt_exist(sake_id):
    if sake_id not in SAKES:
        abort(404, message="Todo {} doesn't exist".format(sake_id))


class SakeController(Resource):
    def get(self):
        docs = sakes_ref.stream()
        reses = [{doc.id: doc.to_dict()} for doc in docs]
        return reses, 200


class SakesController(Resource):
    def get(self):
        docs = sakes_ref.stream()
        reses = [{doc.id: doc.to_dict()} for doc in docs]
        return reses, 200


api.add_resource(SakeController, '/sake')
api.add_resource(SakesController, '/sakes')
