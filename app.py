from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from config import app_config
from models import db, bcrypt


from views.user_views import user_api as user_blueprint


def create_app(env_name):
  """
  Create app
  """
  # app initiliazation
  app = Flask(__name__)
  # cors
  CORS(app, supports_credentials=True)

  app.config.from_object(app_config[env_name])

  bcrypt.init_app(app)


  db.init_app(app)

  migrate = Migrate(app, db)

  app.register_blueprint(user_blueprint, url_prefix='/api/v1/users')


  @app.route('/')
  def index():
    """
    example endpoint
    """
    app.logger.info('App Initiated!')
    return 'Your first route is working on port 5005' + str(migrate)

  return app