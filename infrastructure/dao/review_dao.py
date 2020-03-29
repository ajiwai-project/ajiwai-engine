from config import db

class ReviewDao:
    def __init__(self):
       self.database = db.collection('reviews')


    def find_all(self):
        return self.database.get()

    def register(self, brand_id, text, image_url):
        return self.database.add({
            'brand_id': brand_id,
            'text': text,
            'image_url': image_url
        })
