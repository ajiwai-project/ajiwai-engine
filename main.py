from flask import Flask

from application.controllers import brand_controller, review_controller


app = Flask(__name__)
app.register_blueprint(brand_controller.app, url_prefix='/api/brands')
app.register_blueprint(review_controller.app, url_prefix='/api/reviews')

if __name__ == '__main__':
    app.run(debug=True)
