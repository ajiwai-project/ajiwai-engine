import json

from application.services.review_service import ReviewService

if __name__ == "__main__":

    review_service = ReviewService()
    reviews = review_service.get_reviews()
    fw = open('model/assets/reviews_dump.json', 'w')
    json.dump(reviews, fw, indent=4)
