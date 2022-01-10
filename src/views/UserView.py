from marshmallow import ValidationError
from flask import request, json, Response, Blueprint, g
from ..models.UserModel import UserModel, UserSchema, ValidateSchema
from ..models.StatisticsModel import StatisticsModel
from ..shared.Authentication import Auth
from flask_mail import Message
from flask import current_app
from ..models import mail
import pika
import ssl


user_api        = Blueprint('user_api', __name__)
user_schema     = UserSchema()
validate_schema = ValidateSchema()

@user_api.route('/create', methods=['POST'])
def create():
  if (request.data):
    req_data = request.get_json()
    error = False
    try:
      data = user_schema.load(req_data)
    except ValidationError as err:
      error = {'success':False,'error':err.messages}

    if error:
      return send_response(error, 400)
    
    # check if user already exist in the db
    user_in_db = UserModel.get_by_email(data.get('email'))
    if user_in_db:
      message = {'success':False,'error': 'User already exist, please supply another email address'}
      return send_response(message, 400)

    user = UserModel(data)
    user.save()
        
    user_data = user_schema.dump(user.as_dict())
    add_job(user_id = user_data.get('id'), zip_code = user_data.get('zip_code'))
    
    #token = Auth.generate_token(user_data.get('id'))
    msg = Message('Validation email', sender = 'testcarlos@kaibosmedia.com', recipients = [user_data.get('email')])
    msg.html = "<p>you must click <a href=\""+ current_app.config['WEBSITE_URL'] + \
      "validate_account.html?token="+ user_data.get('activation_key') + \
      "\">this</a> link to validate your account <p>"
    mail.send(msg)
    
    return send_response({'success':True,'id': user_data.get('id')}, 201)
  else:
    message = {'success':False,'error': 'You must speciy the requested values'}
    return send_response(message, 400)

@user_api.route('/validate', methods=['POST'])
def validate():
  if (request.data):
    req_data = request.get_json()
    error = False
    try:
      data = validate_schema.load(req_data)
    except ValidationError as err:
      error = {'success':False,'error':err.messages}

    if error:
      return send_response(error, 400)
    
    # check if user already exist in the db
    user = UserModel.get_by_activation_key(data.get('activation_key'))
    if user:
      user_data = user_schema.dump(user.as_dict())
      if user_data.get('is_active') == False:
        user_data['is_active'] = True
        user_data['password'] = data['password']

        user.update(user_data)
        return send_response({'message': 'Account successfully validated'}, 201)
      else:
        message = {'error': 'Account already active'}
        return send_response(message, 400)
    else:
      message = {'error': 'Invalid activation key'}
      return send_response(message, 400)    
  else:
    message = {'error': 'You must speciy the requested values'}
    return send_response(message, 400)

@user_api.route('/get_all', methods=['GET'])
@Auth.auth_required
def get_all():
  user = UserModel.get_user(g.user.get('id'))
  if getattr(user, 'user_type') != 'admin':
    message = {'success':False,'error': "you do not have the correct permissions to view this content"}
    return send_response(message, 401)

  users = UserModel.get_all_users()
  ser_users = user_schema.dump(users, many=True)
  return send_response(ser_users, 200)

@user_api.route('/<int:user_id>', methods=['GET'])
@Auth.auth_required
def get_a_user(user_id):
  token_user = UserModel.get_user(g.user.get('id'))
  
  #to validate that the current user is the same that asking data
  if getattr(token_user, 'id') == user_id:
    user = UserModel.get_user(g.user.get('id'))
    if not user:
      return send_response({'error': 'user not found'}, 404)
    ser_user = user_schema.dump(user)
    return send_response(ser_user, 200)
  else:
    if getattr(token_user, 'user_type') == 'admin':
      user = UserModel.get_user(user_id)
      if not user:
        return send_response({'error': 'user not found'}, 404)
      ser_user = user_schema.dump(user)
      return send_response(ser_user, 200)
    else:
      return send_response({'error': 'you do not have the correct permissions to ask for this data'}, 404)

@user_api.route('/me', methods=['PUT'])
@Auth.auth_required
def update():
  if request.data:
    req_data = request.get_json()
    error = False
    try:
      data = user_schema.load(req_data,partial=True)
    except ValidationError as err:
      error = {'error':err.messages}

    if error:
      return send_response(error, 400)
      
    user = UserModel.get_user(g.user.get('id'))
    user.update(data)
    ser_user = user_schema.dump(user)

    add_job(user_id = ser_user.get('id'), zip_code = ser_user.get('zip_code'))

    return send_response(ser_user, 200)
  else:
    message = {'error': 'You must speciy the requested values'}
    return send_response(message, 400)

@user_api.route('/me', methods=['GET'])
@Auth.auth_required
def get_me():
  user = UserModel.get_user(g.user.get('id'))
  ser_user = user_schema.dump(user)
  return send_response(ser_user, 200)

@user_api.route('/get_distances', methods=['GET'])
@Auth.auth_required
def get_distances():
  user = UserModel.get_user(g.user.get('id'))
  user_data = user_schema.dump(user)

  if user_data.get('lat') != None and user_data.get('lng') != None:
    data = StatisticsModel.get_distances_from_user(lat=user_data.get('lat'),lng=user_data.get('lng'))
  else:
    return send_response({'error':'can not calculate distances for this user. Try again later'}, 400)
  
  return send_response(data, 200)

@user_api.route('/get_distances/<int:user_id>', methods=['GET'])
@Auth.auth_required
def get_distances_by_user_id(user_id):
  user = UserModel.get_user(g.user.get('id'))
  if getattr(user, 'user_type') != 'admin':
    message = {'success':False,'error': "you do not have the correct permissions to view this content"}
    return send_response(message, 401)

  user = UserModel.get_user(user_id)
  if user:
    user_data = user_schema.dump(user)

    if user_data.get('lat') != None and user_data.get('lng') != None:
      data = StatisticsModel.get_distances_from_user(lat=user_data.get('lat'),lng=user_data.get('lng'))
    else:
      return send_response({'error':'can not calculate distances for this user. Try again later'}, 400)
    
    return send_response(data, 200)
  else:
    return send_response({'error':'user does not exist'}, 400)


@user_api.route('/login', methods=['POST']) 
def login():
  req_data = request.get_json()
  error = False
  try:
    data = user_schema.load(req_data, partial=True)
  except ValidationError as err:
    error = {'success':False,'error':err.messages}
  if error:
    return send_response(error, 400)
  if not data.get('email') or not data.get('password'):
    return send_response({'error': 'you need email and password to sign in'}, 400)
  user = UserModel.get_by_email(data.get('email'))
  if not user:
    return send_response({'error': 'invalid credentials'}, 400)
  if not user.check_hash(data.get('password')):
    return send_response({'error': 'invalid credentials'}, 400)
  ser_data = user_schema.dump(user)
  token = Auth.generate_token(ser_data.get('id'))
  return send_response({'success':True,'token': token}, 200)


def send_response(res, status_code):

  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )

def add_job(user_id,zip_code):
  message = json.dumps({'user_id':user_id,'zip_code':zip_code})
 
  credentials = pika.PlainCredentials(current_app.config['RABBITMQ_USERNAME'], current_app.config['RABBITMQ_PASSWORD'])
  context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
  parameters = pika.ConnectionParameters(host=current_app.config['RABBITMQ_HOST'],
                                        port=current_app.config['RABBITMQ_PORT'],
                                        virtual_host='/',
                                        credentials=credentials,
                                        ssl_options=pika.SSLOptions(context)
                                        )

  connection = pika.BlockingConnection(parameters)


  channel = connection.channel()
  channel.queue_declare(queue='task_queue', durable=True)
  channel.basic_publish(
      exchange='',
      routing_key='task_queue',
      body=message,
      properties=pika.BasicProperties(
          delivery_mode=2,  # make message persistent
      ))
  connection.close()

