from config import memory_reviews_db


class ReviewMemoryDao:
    def __init__(self):
        self.reviews = memory_reviews_db

    def find_all(self):
        return [[id, review] for id, review in self.reviews.items()]

    def register(self, brand_id, text, image_url):
        return None
