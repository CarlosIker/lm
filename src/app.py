#src/app.py

from flask import Flask
from flask_migrate import Migrate

from .config import app_config
from .models import db, bcrypt, mail

# import user_api blueprint
from .views.UserView import user_api as user_blueprint
from .views.BlogpostView import blogpost_api as blogpost_blueprint


def create_app(env_name):  
  # app initiliazation
  app = Flask(__name__)

  app.config.from_object(app_config[env_name])

  # initializing bcrypt and db
  bcrypt.init_app(app)
  db.init_app(app)
  mail.init_app(app)

  migrate = Migrate(app, db)

  app.register_blueprint(user_blueprint, url_prefix='/api/v1/users')
  app.register_blueprint(blogpost_blueprint, url_prefix='/api/v1/blogposts')

  @app.route('/', methods=['GET'])
  def index():
    return 'Test env'

  return app

