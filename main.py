from flask import Flask

from controllers import sake, test


app = Flask(__name__)
app.register_blueprint(test.app, url_prefix='/api')
app.register_blueprint(sake.app, url_prefix='/api')


if __name__ == '__main__':
    app.run(debug=True)
