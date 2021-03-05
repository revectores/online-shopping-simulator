from flask import Flask
from app import app


from app.handler.user.user import user, user_api

app.register_blueprint(user, url_prefix="/user")


@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
