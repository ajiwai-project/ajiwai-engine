from flask import Flask

from application.controllers import brand_controller


app = Flask(__name__)
app.register_blueprint(brand_controller.app, url_prefix='/api')


if __name__ == '__main__':
    app.run(debug=True)
