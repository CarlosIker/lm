import unittest
import os
import json
from ..app import create_app, db
import time
from ..scripts.zip_code_counter import default_test


class UsersTest(unittest.TestCase):
  def test_zone_distance(self):
    """ Test User get by id me """

    test_data = [
      {'lat1':1.1,'lng1':1.1,'lat2':2.1,'lng2':2.1,'result':157.2141563775629},
      {'lat1':32.9697,'lng1':-96.80322,'lat2':29.46786,'lng2':-98.53506,'result':422.73893139401383}
    ]
    
    for r in test_data:
      self.assertEqual(default_test(r), r['result'])
    
if __name__ == "__main__":
  unittest.main() 