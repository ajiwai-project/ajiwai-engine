from config import db
from infrastructure.dao.brand_dao import BrandDao

brands_ref = db.collection('brands')


class BrandRepository:
    def __init__(self):
        self.brand_dao = BrandDao()

    def create(self, name, prefecture, maker, image_url):
        doc = self.brand_dao.register(name, prefecture, maker, image_url)
        doc_snap = doc[1].get()
        return doc_snap.id
