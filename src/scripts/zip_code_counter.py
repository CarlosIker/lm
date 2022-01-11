from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import os
from sqlalchemy.sql import text
import pytest 

def main():
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

#@pytest.fixture
def default_test(test_data):
    Base = automap_base()
    engine = create_engine(os.getenv('DATABASE_TEST_URL'))
    Base.prepare(engine, reflect=True)
    #Statistics = Base.classes.statistics
    db_session = Session(engine)

    #user = db_session.query(Users).with_entities(Users.zip_code,Users.city).first()

    sql = text('''
        CREATE OR REPLACE FUNCTION calculate_distance(lat1 float, lon1 float, lat2 float, lon2 float, units varchar)
        RETURNS float AS $dist$
            DECLARE
                dist float = 0;
                radlat1 float;
                radlat2 float;
                theta float;
                radtheta float;
            BEGIN
                IF lat1 = lat2 OR lon1 = lon2
                    THEN RETURN dist;
                ELSE
                    radlat1 = pi() * lat1 / 180;
                    radlat2 = pi() * lat2 / 180;
                    theta = lon1 - lon2;
                    radtheta = pi() * theta / 180;
                    dist = sin(radlat1) * sin(radlat2) + cos(radlat1) * cos(radlat2) * cos(radtheta);

                    IF dist > 1 THEN dist = 1; END IF;

                    dist = acos(dist);
                    dist = dist * 180 / pi();
                    dist = dist * 60 * 1.1515;

                    IF units = 'K' THEN dist = dist * 1.609344; END IF;
                    IF units = 'N' THEN dist = dist * 0.8684; END IF;

                    RETURN dist;
                END IF;
            END;
        $dist$ LANGUAGE plpgsql;
        ''')
    result = engine.execute(sql)
    
    data = db_session.query(func.calculate_distance(test_data['lat1'],test_data['lng1'],test_data['lat2'],test_data['lng2'],'K')).first()
    
    #print(results)
    engine.dispose()
    return data[0]
    
if __name__ == "__main__":
    main()
    #print(test({'lat1':1.1,'lng1':1.1,'lat2':2.1,'lng2':2.1}))