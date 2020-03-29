
class Review:
    def __init__(self, text, image_url):
        self.text = text
        self.image_url = image_url

    def __str__(self):
        return '%s, %s' % (self.text, self.image_url)
