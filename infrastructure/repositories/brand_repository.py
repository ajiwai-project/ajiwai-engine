from config import db
from infrastructure.dao.brand_dao import BrandDao

brands_ref = db.collection('brands')

class BrandRepository:
    def __init__(self):
        self.brand_dao = BrandDao()

    def create(self, brand_id):
        return brands_ref.add(brand.parse())


    def create(self, name, prefecture, maker, image_url):
        brand = self.brand_dao.find_by_user_id(brand.brand_id)

        if brand is None:
            return False
        
        tmp = self.brand_dao.register(name, prefecture, maker, image_url)
        print(tmp)

