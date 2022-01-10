from marshmallow import fields, Schema, validates_schema, ValidationError, post_load, validate
import datetime
import string    
import random


from . import db, bcrypt

class UserModel(db.Model):
  """
  User Model
  """

  # table name
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  first_name      = db.Column(db.String(128), nullable=False)
  middle_name     = db.Column(db.String(128), nullable=True)
  last_name       = db.Column(db.String(128), nullable=True)
  email           = db.Column(db.String(200), unique=True, nullable=False)
  password        = db.Column(db.String(300), nullable=True)
  zip_code        = db.Column(db.String(10),  nullable=False)
  created_at      = db.Column(db.DateTime)
  modified_at     = db.Column(db.DateTime)
  is_active       = db.Column(db.Boolean, default=False, nullable=False)
  activation_key  = db.Column(db.String(256), nullable=True, unique=True)
  user_type       = db.Column(db.String(20),nullable=True)

  city            = db.Column(db.String(100),nullable=True)
  country         = db.Column(db.String(100),nullable=True)
  state           = db.Column(db.String(100),nullable=True)

  lat             = db.Column(db.String(100),nullable=True)
  lng             = db.Column(db.String(100),nullable=True)


  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.first_name = data.get('first_name')
    self.milddle_name = data.get('middle_name')
    self.last_name = data.get('last_name')

    self.email = data.get('email')

    if data.get('password'):
      self.password = self.__generate_hash(data.get('password'))
    else:
      self.password = self.__generate_hash(''.join(random.choices(string.ascii_uppercase + string.digits, k = 10)))

    self.created_at = datetime.datetime.utcnow()
    self.modified_at = datetime.datetime.utcnow()

    self.is_active = False
    self.activation_key = self.__generate_hash(''.join(random.choices(string.ascii_uppercase + string.digits, k = 10)))

    self.zip_code = data.get('zip_code')

    self.user_type = data.get('user_type')

  def save(self):
    db.session.add(self)
    db.session.commit()

  def update(self, data):
    for key, item in data.items():
      if key == 'password':
        #pass
        #setattr(self, 'password', self.__generate_hash(item))
        self.password = self.__generate_hash(item)
      setattr(self, key, item)
    self.modified_at = datetime.datetime.utcnow()
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  @staticmethod
  def get_all_users():
    return UserModel.query.add_columns(UserModel.id,UserModel.first_name,UserModel.middle_name,UserModel.last_name,
      UserModel.email,UserModel.zip_code,UserModel.created_at,UserModel.is_active,UserModel.user_type,UserModel.lat,UserModel.lng
      ).all()

  @staticmethod
  def get_user(id):
    return UserModel.query.get(id)
  
  @staticmethod
  def get_by_email(value):
    return UserModel.query.filter_by(email=value).first()
  
  @staticmethod
  def get_by_email_password(email,password):
      #return UserModel.query.filter_by(email=email,password=self.__generate_hash(password)).first()
      return UserModel.query.filter_by(email=email,password=password).first()

  @staticmethod
  def get_by_activation_key(value):
    return UserModel.query.filter_by(activation_key=value).first()

  def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

  def __generate_hash(self, password):
    return str(bcrypt.generate_password_hash(password, rounds=10))
  
  def check_hash(self, password):
    return self.password == password
    #return bcrypt.check_password_hash(self.password, password)
  
  def __repr(self):
    return '<id {}>'.format(self.id)

class UserSchema(Schema):
  def validate_zip_code(n):
    if len(n) != 5 and n.isdigit() == False:
      raise ValidationError("Zip code must be 5 digits number")
    return n
  
  id = fields.Int(dump_only=True)
  first_name = fields.Str(required=True)
  middle_name = fields.Str(required=False)
  last_name = fields.Str(required=True)

  email = fields.Email(required=False)
  password = fields.Str(required=False)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)

  is_active = fields.Bool(required=False)
  activation_key  = fields.Str(required=False)
  
  zip_code  = fields.Str(required=True,validate=validate_zip_code)

  lat = fields.Float(required=True)
  lng = fields.Float(required=True)

class ValidateSchema(Schema):
  password = fields.Str(required=True,validate=validate.Length(min=8,max=80))
  activation_key  = fields.Str(required=True)
