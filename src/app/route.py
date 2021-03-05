from flask import Flask, send_from_directory
from app import app


from app.handler.user.user import user, user_api
from app.handler.product.product import product, product_api

app.register_blueprint(user, url_prefix="/user")
app.register_blueprint(product, url_prefix="/product")


@app.route('/')
def index():
    return send_from_directory('templates/', 'index.html')


if __name__ == '__main__':
    app.run()
