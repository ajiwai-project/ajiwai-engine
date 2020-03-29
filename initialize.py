from pprint import pprint
from tqdm import tqdm

from scraping.brands_scr import get_brands_and_reviews_from_saketime
from infrastructure.repositories.brand_repository import BrandRepository
from infrastructure.repositories.review_repository import ReviewRepository

if __name__ == '__main__':
    brand_repository = BrandRepository()
    review_repository = ReviewRepository()

    brands_reviews_map = get_brands_and_reviews_from_saketime()

    progress = tqdm(brands_reviews_map.items())
    progress.set_description('Store Firebase')
    for brand, reviews in progress:
        brand_id = brand_repository.create(
            brand.name,
            brand.prefecture,
            brand.maker,
            'dummy.com'
        )
        for review in reviews:
            review_repository.create(
                brand_id,
                review.text,
                review.image_url
            )
