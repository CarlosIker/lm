from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import os
from sqlalchemy.sql import text

Base = automap_base()
engine = create_engine(os.getenv('DATABASE_URL'), convert_unicode=True)
Base.prepare(engine, reflect=True)
Statistics = Base.classes.statistics
db_session = Session(engine)

#user = db_session.query(Users).with_entities(Users.zip_code,Users.city).first()

sql = text('''
    SELECT
        zip_code,city,
        COUNT(zip_code) AS n_times 
    FROM
        users
    GROUP BY 
        zip_code,city
    ORDER BY 
        n_times DESC
    LIMIT 10;''')
result = engine.execute(sql)

new_data = []
for row in result:
    #session.add(Statistics(title = "Sing", genre_id=2))
    new_data.append(Statistics(id=len(new_data)+1,zip_code=row[0],city=row[1],number_of_registers=row[2]))


db_session.query(Statistics).delete()
db_session.bulk_save_objects(new_data)
db_session.commit()


engine.dispose()