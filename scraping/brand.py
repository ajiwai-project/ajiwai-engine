
class Brand:
    def __init__(self, name, prefecture, maker):
        self.name = name
        self.prefecture = prefecture
        self.maker = maker

    def __str__(self):
        return '%s, %s, %s' % (self.name, self.prefecture, self.maker)