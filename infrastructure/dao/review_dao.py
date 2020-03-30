from config import db


class ReviewDao:
    def __init__(self):
        self.database = db.collection('reviews')

    def find_all(self):
        docs = self.database.get()
        return [[doc.id, doc.to_dict()] for doc in docs]
