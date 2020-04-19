from config import firestore_db
import sys

class BrandDao:

    def __init__(self):
        self.database = firestore_db.collection('brands')

    def parse(self):
        return {
            'name': self.name,
            'prefecture': self.prefecture,
            'maker': self.maker,
            'image_url': self.image_url
        }


    def find_by_brand_id(self, brand_id):
        return self.database.document(brand_id).get().to_dict()


    def find_all(self):
        return self.database.get()


    def register(self, name, prefecture, maker, image_url):
        return self.database.add({
            'name': name,
            'prefecture': prefecture,
            'maker': maker,
            'image_url': image_url
        })
        


