from pprint import pprint

from scraping.brands_scr import get_brands_and_reviews_from_saketime
from repositories.brand_repository import post_brand
from repositories.review_repository import post_review


if __name__ == '__main__':
    brands_reviews_map = get_brands_and_reviews_from_saketime()
    for brand, reviews in brands_reviews_map.items():
        res = post_brand(brand)
        brand_id = res[1].id
        for review in reviews:
            post_review(brand_id, review)
