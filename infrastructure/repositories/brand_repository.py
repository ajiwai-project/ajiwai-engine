from infrastructure.dao.firebase.brand_dao import BrandDao

class BrandRepository:
    def __init__(self):
        self.brand_dao = BrandDao()

    def create(self, name, prefecture, maker, image_url):
        doc = self.brand_dao.register(name, prefecture, maker, image_url)
        doc_snap = doc[1].get()
        return doc_snap.id
