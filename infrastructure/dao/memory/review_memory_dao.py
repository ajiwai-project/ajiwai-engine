from config import memory_reviews_db


class ReviewMemoryDao:
    def __init__(self):
        self.reviews = memory_reviews_db

    def find_all(self):
        return [[review[0], review[1]] for review in self.reviews]

    def register(self, brand_id, text, image_url):
        return None
