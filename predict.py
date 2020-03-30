from application.services.brand_service import BrandService
from pprint import pprint

if __name__ == '__main__':
    brand_service = BrandService()
    res = brand_service.predict('甘くてフルーティ')
    pprint(res)
