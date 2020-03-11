from config import db

reviews_ref = db.collection('reviews')


def save_review(brand_id, review):
    return reviews_ref.add(review.parse(brand_id))


def find_reviews():
    pass
