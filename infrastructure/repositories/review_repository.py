import sys

from config import db
from infrastructure.dao.review_dao import ReviewDao


class ReviewRepository:
    def __init__(self):
        args = sys.argv[1]
        if(args == "local"):
            # TODO configの値によって呼び出すDaoを変える
            self.review_dao = ReviewDao()
        else:
            self.review_dao = ReviewDao()

    def find_all(self):
        return self.review_dao.find_all()

    def create(self, brand_id, text, image_url):
        doc = self.review_dao.register(brand_id, text, image_url)
        doc_snap = doc[1].get()
        return doc_snap.id
