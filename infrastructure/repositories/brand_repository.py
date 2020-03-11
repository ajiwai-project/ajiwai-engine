from config import db

brands_ref = db.collection('brands')

def save_brand(brand):
    return brands_ref.add(brand.parse())

def find_brands():
    pass
