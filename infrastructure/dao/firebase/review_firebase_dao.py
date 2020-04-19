from config import firestore_db


class ReviewFBDao:
    def __init__(self):
        self.database = firestore_db.collection('reviews')

    def find_all(self):
        docs = self.database.get()
        return [[doc.id, doc.to_dict()] for doc in docs]

    def register(self, brand_id, text, image_url):
        return self.database.add({
            'brand_id': brand_id,
            'text': text,
            'image_url': image_url
        })
