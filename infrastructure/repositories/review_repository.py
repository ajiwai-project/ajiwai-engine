from config import db

reviews_ref = db.collection('reviews')


def post_review(brand_id, review):
    return reviews_ref.add(review.parse(brand_id))


def get_reviews():
    pass
