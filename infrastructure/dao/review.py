

class Review:
    def __init__(self, text: str, image_url: str):
        self.brand_id = ''
        self.text = text
        self.image_url = image_url
        self.score = 5 # TODO

    def parse(self, brand_id):
        return {
            'brand_id': brand_id,
            'text': self.text,
            'image_url': self.image_url
        }
