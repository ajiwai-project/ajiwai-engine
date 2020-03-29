from config import db

class ReviewDao:
    def __init__(self):
       self.database = db.collection('reviews')


    def find_all(self):
        return self.database.get()
