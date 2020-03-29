import sys
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from infrastructure.dao.review import Review
from infrastructure.dao.brand import Brand

HOST = 'https://www.saketime.jp'


def get_brands_and_reviews_from_saketime():
    brands_reviews_map = {}

    for idx in tqdm(range(1, 51)):
        URL = HOST + '/brands/' + str(idx)
        soup = BeautifulSoup(requests.get(URL).content, 'lxml')
        try:
            # ブランド名
            brand_header_dom = soup.find('section', id='brand-header')
            brand_name = brand_header_dom.get('brandname')

            # メーカー名
            brand_info_dom = brand_header_dom.find('p', class_='brandinfo')
            brand_prefecture = brand_info_dom.find(class_='pref_link').string.strip('\n').strip()
            brand_maker = brand_info_dom.find(href='#maker').string

            review_num_dom = brand_header_dom.find('p', class_='review_num')
            review_num_dom.find('i').decompose()
            _, review_num = review_num_dom.text.split('：')
            review_num = int(review_num.strip())

            brand = Brand(brand_name, brand_prefecture, brand_maker)
            
            # レビュー
            loop_cnt = int(review_num / 20) + 1
            reviews = []
            for cnt in range(1, loop_cnt + 1):
                PAGE_URL = URL if loop_cnt == 0 else URL + '/page:' + str(cnt)
                page_soup = BeautifulSoup(
                    requests.get(PAGE_URL).content, 'lxml')
                reviews_dom = page_soup.find(id='review').find_all('li')
                for review_dom in reviews_dom:
                    content = review_dom.find(class_='r-body').text.strip()
                    img_url_dom = review_dom.find(class_='review-img')
                    img_url = img_url_dom.find('img').get('data-original')
                    review = Review(content, HOST + '/' + img_url)
                    reviews.append(review)
            brands_reviews_map[brand] = reviews

        except AttributeError as e:
            print(e)
            print('idx:', idx, 'の日本酒がありませんでした')
        except ValueError as e:
            print(e)
            print('idx:', idx, 'のレビューがありませんでした')

    return brands_reviews_map
