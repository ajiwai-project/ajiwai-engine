
from infrastructure.dao.review import Review


class Brand:
    def __init__(self, name: str, prefecture: str, maker: str):
        self.id = ''
        self.name = name
        self.prefecture = prefecture
        self.maker = maker
        self.image_url = 'http://dummy' # TODO

    def parse(self):
        return {
            'name': self.name,
            'prefecture': self.prefecture,
            'maker': self.maker,
            'image_url': self.image_url
        }
