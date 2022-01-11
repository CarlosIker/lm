import unittest
import os
import json
from ..app import create_app, db


class UsersTest(unittest.TestCase):
  @classmethod
  def setUpClass(self):
    self.app = create_app("development")
    self.client = self.app.test_client
    
    #valid
    self.user1 = {
      'email': 'carlosatenciof@gmail.com',
      'password': '12345678'
    }
    with self.app.app_context():
      # create all tables
      #db.create_all()
      pass
  
  def test_user_get_by_id_me(self):
    """ Test User get by id me """

    res = self.client().post('/api/v1/users/login', headers={'Content-Type': 'application/json'}, data=json.dumps(self.user1))
    self.assertEqual(res.status_code, 200)
    api_token = json.loads(res.data).get('token')
    
    res = self.client().get('/api/v1/users/get_distances', headers={'Content-Type': 'application/json', 'api-token': api_token})
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertTrue(json_data[0].get('number_of_registers'))
    self.assertTrue(json_data[0].get('distance'))
    self.assertTrue(json_data[0].get('city'))
    self.assertTrue(json_data[0].get('id'))
    self.assertTrue(json_data[0].get('zip_code'))



  @classmethod
  def tearDownClass(self):
    """
    Tear Down
    """
    with self.app.app_context():
      #db.session.remove()
      #db.drop_all()
      pass

if __name__ == "__main__":
  unittest.main() 