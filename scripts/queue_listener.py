import pika
import time
import os
from dotenv import load_dotenv, find_dotenv
import ssl
import json
import requests
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine


sleepTime = 1
print(' [*] Sleeping for ', sleepTime, ' seconds.')
time.sleep(1)

print(' [*] Connecting to server ...')


credentials = pika.PlainCredentials(os.getenv('RABBITMQ_USERNAME'), os.getenv('RABBITMQ_PASSWORD'))
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
parameters = pika.ConnectionParameters(host=os.getenv('RABBITMQ_HOST'),
                                    port=os.getenv('RABBITMQ_PORT'),
                                    virtual_host='/',
                                    credentials=credentials,
                                    ssl_options=pika.SSLOptions(context)
                                    )
connection = pika.BlockingConnection(parameters)

channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)

print(' [*] Waiting for messages.')


def callback(ch, method, properties, body):
    print(" [x] Received %s" % body)
    message = json.loads(body.decode())    
    '''
    url = os.getenv('ZIP_CODE_API_BASE_URL') + os.getenv('ZIP_CODE_API_KEY') + '/info.json/' + message['zip_code'] +'/degrees' 
    r = requests.get(url)
    data = r.json()
    '''
    data = json.loads('''{"zip_code":"32003","lat":30.095583,"lng":-81.710086,"city":"Fleming Island","state":"FL","timezone":{"timezone_identifier":"America/New_York","timezone_abbr":"EST","utc_offset_sec":-18000,"is_dst":"F"},"acceptable_city_names":[{"city":"Fleming Isle","state":"FL"},{"city":"Orange Park","state":"FL"},{"city":"Orange Pk","state":"FL"}],"area_codes":[904]}''')
    
    Base = automap_base()
    
    #it has 'user' set up
    engine = create_engine(os.getenv('DATABASE_URL'), convert_unicode=True)

    # reflect the table
    Base.prepare(engine, reflect=True)

    # mapped classes are now created with names by default
    # matching that of the table name.
    Users = Base.classes.users
    
    db_session = Session(engine)

    user = db_session.query(Users).get(message['user_id'])
    
    user.city = data['city'] if 'city' in data else None
    user.country = data['country'] if 'country' in data else None
    user.state = data['state'] if 'state' in data else None
    user.lat = data['lat'] if 'lat' in data else None
    user.lng = data['lng'] if 'lng' in data else None

    db_session.commit()

    engine.dispose()

    print(" [x] Done")
    time.sleep(5)

    #ch.basic_ack(delivery_tag=method.delivery_tag)
    ch.basic_nack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)
channel.start_consuming()