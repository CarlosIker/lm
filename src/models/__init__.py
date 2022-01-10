#src/models/__init__.py

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail

# initialize our db
db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()

#from .UserModel import UserModel, UserSchema
from .UserModel import UserModel, UserSchema
from .StatisticsModel import *