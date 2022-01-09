import pika
import time
import os
from dotenv import load_dotenv, find_dotenv
import ssl
import json

sleepTime = 10
print(' [*] Sleeping for ', sleepTime, ' seconds.')
time.sleep(30)

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
    message = json.dumps(body.decode())    
    print(message)
    print(" [x] Done")

    #ch.basic_ack(delivery_tag=method.delivery_tag)
    ch.basic_nack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)
channel.start_consuming()