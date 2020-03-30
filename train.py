from pprint import pprint
import pandas as pd

from application.services.review_service import ReviewService

if __name__ == '__main__':
    review_service = ReviewService()
    reviews = review_service.get_reviews()
    reviews_df = [[review[1]['brand_id'], review[1]['text']] for review in reviews]
    df = pd.DataFrame(reviews_df, columns=['brand_id', 'review'])
    print(df)
    
