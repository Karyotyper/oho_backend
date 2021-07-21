import os

from app import  create_app

env_name = "development"
app = create_app(env_name)

if __name__ == '__main__':
    app.run()

