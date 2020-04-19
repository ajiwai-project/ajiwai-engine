import sys

from infrastructure.dao.firebase.review_firebase_dao import ReviewFBDao
from infrastructure.dao.memory.review_memory_dao import ReviewMemoryDao



class ReviewRepository:
    def __init__(self):
        args = sys.argv[1]
        if(args == "local"):
            self.review_dao = ReviewMemoryDao()
        else:
            self.review_dao = ReviewFBDao()

    def find_all(self):
        return self.review_dao.find_all()

    def create(self, brand_id, text, image_url):
        doc = self.review_dao.register(brand_id, text, image_url)
        doc_snap = doc[1].get()
        return doc_snap.id
