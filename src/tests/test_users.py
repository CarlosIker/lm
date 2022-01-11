import unittest
import os
import json
from ..app import create_app, db
import time

class UsersTest(unittest.TestCase):
  @classmethod
  def setUpClass(self):
    self.app = create_app("testing")
    self.client = self.app.test_client
    
  @classmethod
  def tearDownClass(self):
    pass

  def setUp(self):
    print('set up')
    #general valid password
    self.password = '123456789'

    #valid data
    self.user1 = {
      'first_name': 'Carlos',
      'last_name': 'Atencio',
      'email': 'testcarlosiker@gmail.com',
      'zip_code': '32244'
    }

    #data to update
    self.user2 = {
      'first_name': 'Paola',
      'last_name':'Atencio'
    }

    with self.app.app_context():
      #create all tables
      db.create_all()
      #pass
    
  def tearDown(self):
    print('tear down')
    with self.app.app_context():
      db.session.remove()
      db.drop_all()
  
  def test_user_creation(self):
    """ test user creation with valid credentials """

    res = self.client().post('/api/v1/users/create', headers={'Content-Type': 'application/json'}, data=json.dumps(self.user1))
    json_data = json.loads(res.data)
    self.assertTrue(json_data.get('id'),res.data)
    self.assertTrue(json_data.get('first_name'))
    self.assertTrue(json_data.get('last_name'))
    self.assertTrue(json_data.get('email'))
    self.assertTrue(json_data.get('activation_key'))
    self.assertEqual(res.status_code, 201)

  def test_user_creation_with_existing_email(self):
    """ test user creation with already existing email"""
    
    res = self.client().post('/api/v1/users/create', headers={'Content-Type': 'application/json'}, data=json.dumps(self.user1))
    self.assertEqual(res.status_code, 201)
    res = self.client().post('/api/v1/users/create', headers={'Content-Type': 'application/json'}, data=json.dumps(self.user1))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 400)
    self.assertTrue(json_data.get('error'))

  def test_user_creation_with_invalid_email(self):
    """ test user creation with invalid email"""
    
    #case 1
    data = self.user1
    data['email'] = 'test.com'
    res = self.client().post('/api/v1/users/create', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 400)
    self.assertTrue(json_data.get('error',{}).get('email'))

    #case 2
    data = self.user1
    data['email'] = 'test@test'
    res = self.client().post('/api/v1/users/create', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 400)
    self.assertTrue(json_data.get('error',{}).get('email'))

    #case 3
    data = self.user1
    data['email'] = '1@3'
    res = self.client().post('/api/v1/users/create', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 400)
    self.assertTrue(json_data.get('error',{}).get('email'))

    #case 4
    data = self.user1
    data['email'] = 'carlos!test.com'
    res = self.client().post('/api/v1/users/create', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 400)
    self.assertTrue(json_data.get('error',{}).get('email'))

  def test_user_creation_with_no_email(self):
    """ test user creation with no email """
    data = self.user1
    del data['email']
    res = self.client().post('/api/v1/users/create', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 400)
    self.assertTrue(json_data.get('error',{}).get('email'))
  
  def test_user_creation_with_empty_request(self):
    """ test user creation with empty request """

    res = self.client().post('/api/v1/users/create', headers={'Content-Type': 'application/json'}, data=json.dumps({}))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 400)

  def test_user_creation_with_invalid_zip_code(self):
    """ test user creation with invalid zip code"""
    data = self.user1

    #case 1
    data['zip_code'] = 'a1234'
    res = self.client().post('/api/v1/users/create', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 400)
    self.assertTrue(json_data.get('error',{}).get('zip_code'))

    #case 2
    data['zip_code'] = '1'
    res = self.client().post('/api/v1/users/create', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 400)
    self.assertTrue(json_data.get('error',{}).get('zip_code'))

    #case 3
    data['zip_code'] = 'abcde'
    res = self.client().post('/api/v1/users/create', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 400)
    self.assertTrue(json_data.get('error',{}).get('zip_code'))

    #case 4
    data['zip_code'] = 'asd'
    res = self.client().post('/api/v1/users/create', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 400)
    self.assertTrue(json_data.get('error',{}).get('zip_code'))

    #case 5
    data['zip_code'] = '123-4'
    res = self.client().post('/api/v1/users/create', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 400)
    self.assertTrue(json_data.get('error',{}).get('zip_code'))

  def test_user_creation_with_no_zip_code(self):
    """ test user creation with no zip code"""
    data = self.user1
    del data['zip_code']

    res = self.client().post('/api/v1/users/create', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 400)
    self.assertTrue(json_data.get('error',{}).get('zip_code'))

  def test_user_validation_with_no_password(self):
    """ test user validation with no password"""

    #create
    res = self.client().post('/api/v1/users/create', headers={'Content-Type': 'application/json'}, data=json.dumps(self.user1))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 201)

    data = {
            "activation_key":json_data.get('activation_key')
        }

    #validate
    res = self.client().post('/api/v1/users/validate', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 400)
    self.assertTrue(json_data.get('error',{}).get('password'))

  def test_user_validation_with_invalid_password(self):
    """ test user validation with invalid password """
    #create
    res = self.client().post('/api/v1/users/create', headers={'Content-Type': 'application/json'}, data=json.dumps(self.user1))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 201)

    data = {
            'activation_key':json_data.get('activation_key'),
            'password':'1234'
        }

    #validate
    res = self.client().post('/api/v1/users/validate', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 400)
    self.assertTrue(json_data.get('error',{}).get('password'))

  def test_user_validation_with_no_activation_key(self):
    """ test user validation with no activation key """
    
    data = {
            "password":self.password
        }
   
    #validate
    res = self.client().post('/api/v1/users/validate', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 400)
    self.assertTrue(json_data.get('error',{}).get('activation_key'))
  
  def test_user_validation_with_invalid_activation_key(self):
    """ test user validation with invalid activation key """
    
    #create
    res = self.client().post('/api/v1/users/create', headers={'Content-Type': 'application/json'}, data=json.dumps(self.user1))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 201)
    
    data = {
            "activation_key":'12345',
            "password":self.password
        } 

    #validate
    res = self.client().post('/api/v1/users/validate', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 400)
    self.assertTrue(json_data.get('error'))

  def test_user_validation_with_valid_data(self):
    """ test user validation with valid data """
    
    #create
    res = self.client().post('/api/v1/users/create', headers={'Content-Type': 'application/json'}, data=json.dumps(self.user1))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 201)

    data = {
            "activation_key":json_data.get('activation_key'),
            "password":self.password
        }

    #validate 
    res = self.client().post('/api/v1/users/validate', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 201,json.dumps(data))
    self.assertTrue(json_data.get('message'))

  def test_user_validation_already_active_account(self):
    """ test user validation with already active account data """
    #create
    res = self.client().post('/api/v1/users/create', headers={'Content-Type': 'application/json'}, data=json.dumps(self.user1))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 201)

    data = {
            "activation_key":json_data.get('activation_key'),
            "password":self.password
        } 

    #validate 1
    res = self.client().post('/api/v1/users/validate', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 201,json.dumps(data))
    
    #validate2
    res = self.client().post('/api/v1/users/validate', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 400)
    self.assertTrue(json_data.get('error'))

  def test_user_login(self):
    """ User Login Tests """

    #create
    res = self.client().post('/api/v1/users/create', headers={'Content-Type': 'application/json'}, data=json.dumps(self.user1))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 201)
    
    data = {
            "activation_key":json_data.get('activation_key'),
            "password":self.password
        } 

    #validate
    res = self.client().post('/api/v1/users/validate', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 201,json.dumps(data))

    data = {
            "email":self.user1['email'],
            "password":self.password
        } 

    #login
    res = self.client().post('/api/v1/users/login', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    json_data = json.loads(res.data)
    self.assertTrue(json_data.get('token'))
    self.assertEqual(res.status_code, 200)

    self.api_token = json_data.get('token')

  def test_user_login_with_invalid_password(self):
    """ User Login Tests with invalid credentials """
    #create
    res = self.client().post('/api/v1/users/create', headers={'Content-Type': 'application/json'}, data=json.dumps(self.user1))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 201)
    
    data = {
      'password': 'test',
      'email': self.user1['email'],
    }

    #login
    res = self.client().post('/api/v1/users/login', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    json_data = json.loads(res.data)
    self.assertEqual(json_data.get('error'), 'invalid credentials')
    self.assertEqual(res.status_code, 400)

  def test_user_login_with_invalid_email(self):
    """ User Login Tests with invalid credentials """

    #create
    res = self.client().post('/api/v1/users/create', headers={'Content-Type': 'application/json'}, data=json.dumps(self.user1))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 201)

    data = {
      'password': self.password,
      'email': 'carlostest123@mail.com',
    }
    res = self.client().post('/api/v1/users/login', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    json_data = json.loads(res.data)
    self.assertEqual(json_data.get('error'), 'invalid credentials')
    self.assertEqual(res.status_code, 400)
  
  def test_user_get_me(self):
    """ Test User Get Me """
    
    #create
    res = self.client().post('/api/v1/users/create', headers={'Content-Type': 'application/json'}, data=json.dumps(self.user1))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 201)

    data = {
            "activation_key":json_data.get('activation_key'),
            "password":self.password
        }

    #validate
    res = self.client().post('/api/v1/users/validate', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 201,json.dumps(data))

    data = {
            "email":self.user1['email'],
            "password":self.password
        }

    #login
    res = self.client().post('/api/v1/users/login', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    self.assertEqual(res.status_code, 200)
    api_token = json.loads(res.data).get('token')

    #get me
    res = self.client().get('/api/v1/users/me', headers={'Content-Type': 'application/json', 'api-token': api_token})
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(json_data.get('email'), self.user1['email'])
    self.assertEqual(json_data.get('first_name'), self.user1['first_name'])
    self.assertEqual(json_data.get('last_name'), self.user1['last_name'])
    self.assertEqual(json_data.get('zip_code'), self.user1['zip_code'])

  def test_user_get_me_updated_city(self):
    """ Test User Get Me with update city """
    #create
    res = self.client().post('/api/v1/users/create', headers={'Content-Type': 'application/json'}, data=json.dumps(self.user1))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 201)

    data = {
            "activation_key":json_data.get('activation_key'),
            "password":self.password
        }

    #validate
    res = self.client().post('/api/v1/users/validate', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 201,json.dumps(data))

    data = {
            "email":self.user1['email'],
            "password":self.password
        }
        
    #login
    res = self.client().post('/api/v1/users/login', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    self.assertEqual(res.status_code, 200)
    api_token = json.loads(res.data).get('token')
    time.sleep(5)

    res = self.client().get('/api/v1/users/me', headers={'Content-Type': 'application/json', 'api-token': api_token})
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(json_data.get('city'), 'Fleming Island')

  def test_user_update_me(self):
    """ Test User Update Me """
    #create
    res = self.client().post('/api/v1/users/create', headers={'Content-Type': 'application/json'}, data=json.dumps(self.user1))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 201)

    data = {
            "activation_key":json_data.get('activation_key'),
            "password":self.password
        }

    #validate
    res = self.client().post('/api/v1/users/validate', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 201,json.dumps(data))

    data = {
            "email":self.user1['email'],
            "password":self.password
        }
        
    #login
    res = self.client().post('/api/v1/users/login', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    self.assertEqual(res.status_code, 200)
    api_token = json.loads(res.data).get('token')

    data = self.user1
    data['first_name'] = self.user2['first_name']
    data['last_name'] = self.user2['last_name'] 

    #update
    res = self.client().put('/api/v1/users/me', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(self.user2))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    
    #get me
    res = self.client().get('/api/v1/users/me', headers={'Content-Type': 'application/json', 'api-token': api_token})
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(json_data.get('first_name'), self.user2['first_name'])
    self.assertEqual(json_data.get('last_name'), self.user2['last_name'])

  def test_user_get_by_id_me(self):
    """ Test User get by id me """

    #create
    res = self.client().post('/api/v1/users/create', headers={'Content-Type': 'application/json'}, data=json.dumps(self.user1))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 201,self.user1)
    
    data = {
            "activation_key":json_data.get('activation_key'),
            "password":self.password
        }

    #validate
    res = self.client().post('/api/v1/users/validate', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 201,json.dumps(data))

    data = {
            "email":self.user1['email'],
            "password":self.password
        }
        
    #login
    res = self.client().post('/api/v1/users/login', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    self.assertEqual(res.status_code, 200)
    api_token = json.loads(res.data).get('token')


    #get me
    res = self.client().get('/api/v1/users/me', headers={'Content-Type': 'application/json', 'api-token': api_token})
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    user_id = json.loads(res.data).get('id')
    
    #get by id
    res = self.client().get('/api/v1/users/'+str(user_id), headers={'Content-Type': 'application/json', 'api-token': api_token})
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(json_data.get('first_name'), self.user1['first_name'])
    self.assertEqual(json_data.get('last_name'), self.user1['last_name'])


if __name__ == "__main__":
  unittest.main() 