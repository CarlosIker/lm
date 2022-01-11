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

    self.activation_key = '123'
    self.password       = '123456789'
    self.api_token      = '' 
    self.user_id        = 1
    
    #valid
    self.user0 = {
      'first_name': 'Carlos',
      'last_name': 'Carlos',
      'email': 'testcarlosiker@gmail.com',
      'zip_code': '32244'
    }

    #valid
    self.user1 = {
      'first_name': 'Carlos',
      'last_name': 'Carlos',
      'email': 'carlosatenciof@gmail.com',
      'zip_code': '32244'
    }

    #repeated email
    self.user2 = {
      'first_name': 'Carlos',
      'last_name':'Atencio',
      'email': 'carlos@email.com',
      'zip_code':'32244'
    }

    #invalid email
    self.user3 = {
      'first_name': 'Carlos',
      'last_name':'Atencio',
      'email': 'carlosemail.com',
      'zip_code':'32244'
    }

    #no email
    self.user4 = {
      'first_name': 'Carlos',
      'last_name':'Atencio',
      'zip_code':'32244'
    }

    #invalid zip_code
    self.user5 = {
      'first_name': 'Carlos',
      'last_name':'Atencio',
      'email': 'carlos12@email.com',
      'zip_code':'a1234'
    }

    #no zip_code
    self.user6 = {
      'first_name': 'Carlos',
      'last_name':'Atencio',
      'email':'testing@email.com'
    }

    #invalid credentials
    self.user7 = {
      'first_name': 'Carlos',
      'last_name':'Atencio',
      'email':'testing@email.com',
      'zip_code':'12345'
    }
    #data to update
    self.user8 = {
      'first_name': 'Paola',
      'last_name':'Atencio'
    }



    with self.app.app_context():
      #create all tables
      db.create_all()
      #pass
  
  """USER CREATION"""
  def test_a_user_creation(self):
    """ test user creation with valid credentials """

    res = self.client().post('/api/v1/users/create', headers={'Content-Type': 'application/json'}, data=json.dumps(self.user1))
    json_data = json.loads(res.data)
    self.assertTrue(json_data.get('id'))
    self.assertTrue(json_data.get('first_name'))
    self.assertTrue(json_data.get('last_name'))
    self.assertTrue(json_data.get('email'))
    self.assertTrue(json_data.get('activation_key'))
    self.assertEqual(res.status_code, 201)

    self.activation_key = json_data.get('activation_key')
    self.user_id = json_data.get('id')

    

  def test_user_creation_with_existing_email(self):
    """ test user creation with already existing email"""
    
    res = self.client().post('/api/v1/users/create', headers={'Content-Type': 'application/json'}, data=json.dumps(self.user2))
    self.assertEqual(res.status_code, 201)
    res = self.client().post('/api/v1/users/create', headers={'Content-Type': 'application/json'}, data=json.dumps(self.user2))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 400)
    self.assertTrue(json_data.get('error'))

  def test_user_creation_with_invalid_email(self):
    """ test user creation with invalid email"""

    res = self.client().post('/api/v1/users/create', headers={'Content-Type': 'application/json'}, data=json.dumps(self.user3))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 400)
    self.assertTrue(json_data.get('error',{}).get('email'))

  def test_user_creation_with_no_email(self):
    """ test user creation with no email """
   
    res = self.client().post('/api/v1/users/create', headers={'Content-Type': 'application/json'}, data=json.dumps(self.user4))
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
    data = self.user5

    data['zip_code'] = 'a1234'
    res = self.client().post('/api/v1/users/create', headers={'Content-Type': 'application/json'}, data=json.dumps(self.user5))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 400)
    self.assertTrue(json_data.get('error',{}).get('zip_code'))

    data['zip_code'] = '1'
    res = self.client().post('/api/v1/users/create', headers={'Content-Type': 'application/json'}, data=json.dumps(self.user5))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 400)
    self.assertTrue(json_data.get('error',{}).get('zip_code'))

    data['zip_code'] = 'abcde'
    res = self.client().post('/api/v1/users/create', headers={'Content-Type': 'application/json'}, data=json.dumps(self.user5))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 400)
    self.assertTrue(json_data.get('error',{}).get('zip_code'))

    data['zip_code'] = 'asd'
    res = self.client().post('/api/v1/users/create', headers={'Content-Type': 'application/json'}, data=json.dumps(self.user5))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 400)
    self.assertTrue(json_data.get('error',{}).get('zip_code'))

    data['zip_code'] = '123-4'
    res = self.client().post('/api/v1/users/create', headers={'Content-Type': 'application/json'}, data=json.dumps(self.user5))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 400)
    self.assertTrue(json_data.get('error',{}).get('zip_code'))

  def test_user_creation_with_no_zip_code(self):
    """ test user creation with no zip code"""
   
    res = self.client().post('/api/v1/users/create', headers={'Content-Type': 'application/json'}, data=json.dumps(self.user6))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 400)
    self.assertTrue(json_data.get('error',{}).get('zip_code'))




  def test_b_user_validation_with_no_password(self):
    """ test user validation with no password"""

    data = {
            "activation_key":self.activation_key
        }
   
    res = self.client().post('/api/v1/users/validate', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 400)
    self.assertTrue(json_data.get('error',{}).get('password'))

  def test_c_user_validation_with_invalid_password(self):
    """ test user validation with invalid password """
    
    data = {
            "activation_key":self.activation_key,
            "password":'1234'
        }
   
    res = self.client().post('/api/v1/users/validate', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 400)
    self.assertTrue(json_data.get('error',{}).get('password'))

  def test_d_user_validation_with_no_activation_key(self):
    """ test user validation with no activation key """

    data = {
            "password":self.password
        }
   
    res = self.client().post('/api/v1/users/validate', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 400)
    self.assertTrue(json_data.get('error',{}).get('activation_key'))
  
  def test_user_validation_with_invalid_activation_key(self):
    """ test user validation with invalid activation key """
    data = {
            "activation_key":'12345',
            "password":self.password
        } 

    res = self.client().post('/api/v1/users/validate', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 400)
    self.assertTrue(json_data.get('error'))

  def test_e_user_validation_with_valid_data(self):
    """ test user validation with valid data """
    res = self.client().post('/api/v1/users/create', headers={'Content-Type': 'application/json'}, data=json.dumps(self.user0))
    json_data = json.loads(res.data)
    self.assertTrue(json_data.get('id'))
    self.assertTrue(json_data.get('first_name'))
    self.assertTrue(json_data.get('last_name'))
    self.assertTrue(json_data.get('email'))
    self.assertTrue(json_data.get('activation_key'))
    self.assertEqual(res.status_code, 201)

    data = {
            "activation_key":json_data.get('activation_key'),
            "password":self.password
        } 
    print(data)
   
    res = self.client().post('/api/v1/users/validate', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 201,json.dumps(data))
    self.assertTrue(json_data.get('message'))

  def test_f_user_validation_already_active_account(self):
    """ test user validation with already active account data """

    data = {
            "activation_key":self.activation_key,
            "password":self.password
        } 
   
    res = self.client().post('/api/v1/users/validate', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 400)
    self.assertTrue(json_data.get('error'))

  def test_g_user_login(self):
    """ User Login Tests """
    data = {
            "email":self.user0['email'],
            "password":self.password
        } 

    res = self.client().post('/api/v1/users/login', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    json_data = json.loads(res.data)
    self.assertTrue(json_data.get('token'))
    self.assertEqual(res.status_code, 200)

    self.api_token = json_data.get('token')

  def test_h_user_login_with_invalid_password(self):
    """ User Login Tests with invalid credentials """
    data = {
      'password': 'test',
      'email': self.user1['email'],
    }

    res = self.client().post('/api/v1/users/login', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    json_data = json.loads(res.data)
    self.assertEqual(json_data.get('error'), 'invalid credentials')
    self.assertEqual(res.status_code, 400)

  def test_user_login_with_invalid_email(self):
    """ User Login Tests with invalid credentials """
    data = {
      'password': self.password,
      'email': 'carlostest123@mail.com',
    }
    res = self.client().post('/api/v1/users/login', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    json_data = json.loads(res.data)
    self.assertEqual(json_data.get('error'), 'invalid credentials')
    self.assertEqual(res.status_code, 400)
  

  def test_i_user_get_me(self):
    """ Test User Get Me """

    data = {
            "email":self.user0['email'],
            "password":self.password
        } 

    res = self.client().post('/api/v1/users/login', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    self.assertEqual(res.status_code, 200)
    api_token = json.loads(res.data).get('token')

    res = self.client().get('/api/v1/users/me', headers={'Content-Type': 'application/json', 'api-token': api_token})
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(json_data.get('email'), self.user0['email'])
    self.assertEqual(json_data.get('first_name'), self.user0['first_name'])
    self.assertEqual(json_data.get('last_name'), self.user0['last_name'])
    self.assertEqual(json_data.get('zip_code'), self.user0['zip_code'])

  def test_j_user_get_me_updated_city(self):
    """ Test User Get Me with update city """
    time.sleep(5)
    data = {
            "email":self.user0['email'],
            "password":self.password
        } 

    res = self.client().post('/api/v1/users/login', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    self.assertEqual(res.status_code, 200)
    api_token = json.loads(res.data).get('token')

    res = self.client().get('/api/v1/users/me', headers={'Content-Type': 'application/json', 'api-token': api_token})
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(json_data.get('city'), 'Fleming Island')

  def test_k_user_update_me(self):
    """ Test User Update Me """
    data = {
            "email":self.user0['email'],
            "password":self.password
        } 

    res = self.client().post('/api/v1/users/login', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    self.assertEqual(res.status_code, 200)
    api_token = json.loads(res.data).get('token')
    
    res = self.client().put('/api/v1/users/me', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(self.user8))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(json_data.get('first_name'), self.user8['first_name'])
    self.assertEqual(json_data.get('last_name'), self.user8['last_name'])

  def test_l_user_get_by_id_me(self):
    """ Test User get by id me """
    data = {
            "email":self.user0['email'],
            "password":self.password
        } 

    res = self.client().post('/api/v1/users/login', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    self.assertEqual(res.status_code, 200)
    api_token = json.loads(res.data).get('token')
    
    res = self.client().get('/api/v1/users/2', headers={'Content-Type': 'application/json', 'api-token': api_token})
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(json_data.get('first_name'), self.user8['first_name'])
    self.assertEqual(json_data.get('last_name'), self.user8['last_name'])
  
  
  @classmethod
  def tearDownClass(self):
    """
    Tear Down
    """
    with self.app.app_context():
      db.session.remove()
      db.drop_all()
      #pass

if __name__ == "__main__":
  unittest.main() 