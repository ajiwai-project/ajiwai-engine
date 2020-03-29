from pprint import pprint

from scraping.brands_scr import get_brands_and_reviews_from_saketime
from infrastructure.repositories.brand_repository import save_brand
from infrastructure.repositories.review_repository import save_review


if __name__ == '__main__':
    brands_reviews_map = get_brands_and_reviews_from_saketime()
    for brand, reviews in brands_reviews_map.items():
        res = save_brand(brand)
        brand_id = res[1].id
        for review in reviews:
            save_review(brand_id, review)
