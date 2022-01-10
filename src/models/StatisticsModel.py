from . import db, bcrypt
from sqlalchemy import func
from .UserModel import UserModel

class StatisticsModel(db.Model):
  """
  Statistics Model
  """

  # table name
  __tablename__ = 'statistics'

  id = db.Column(db.Integer, primary_key=True)
  zip_code              = db.Column(db.String(128), nullable=False)
  city                  = db.Column(db.String(128), nullable=True)
  number_of_registers   = db.Column(db.String(128), nullable=True)

  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.zip_code               = data.get('zip_code')
    self.city                   = data.get('city')
    self.number_of_registers    = data.get('number_of_registers')
  def get_all():
    return StatisticsModel.query.all()
  
  @staticmethod
  def get_distances_from_user(lat, lng):
    statistics_table_name   = StatisticsModel.__table__.name
    user_table_name         = UserModel.__table__.name
    engine = db.get_engine()

    query = '''
        SELECT *, calculate_distance(
			(select lat from {user} u where u.zip_code = s.zip_code limit 1)::float, 
			(select lat from {user} u where u.zip_code = s.zip_code limit 1)::float, 
			{lat} , 
			{lng} , 
            'K')
        FROM {s} s
    '''.format(user = user_table_name, lat = lat, lng=lng, s = statistics_table_name)

    res = db.engine.execute(query)
    #res = StatisticsModel.query([db.func.calculate_distance(10.6300312, -71.8055019, lat, lng, 'K')])
    #res = engine.execute(query).fetchall()

    #res = db.session.query( db.func.calculate_distance(10.6300312, -71.8055019, lat, lgn, 'K') ).all()
    data = []
    for entry in res:
        data.append({'id':entry[0],'zip_code':entry[1],'city':entry[2],'number_of_registers':entry[3],'distance':entry[4]})
    return data