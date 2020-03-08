from application import db

brands_ref = db.collection('brands')

def post_brand(brand):
    return brands_ref.add(brand.parse())


def get_brands():
    pass
