from configparser import ConfigParser
import os

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from kafka.admin import KafkaAdminClient, NewTopic
from kafka import KafkaConsumer
import json
import datetime
import pytz
import psycopg2

KAFKA_HOST = os.environ.get('KAFKA_HOST', 'localhost')
KAFKA_PORT = os.environ.get('KAFKA_PORT', '9092')

POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT', '5432')
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'postgres')
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'psat')

def initialize_topic():
    topic_name = "weather-data-pipeline"
    new_topic = NewTopic(name=topic_name, num_partitions=1, replication_factor=1)
    admin_client = KafkaAdminClient(bootstrap_servers=f'{KAFKA_HOST}:{KAFKA_PORT}')
    admin_client.create_topics(new_topics=[new_topic], validate_only=False)


# initialize_topic()

# connect to the PostgreSQL server
conn = psycopg2.connect(host=POSTGRES_HOST, port=POSTGRES_PORT, database=POSTGRES_DB,
                        user=POSTGRES_USER, password=POSTGRES_PASSWORD)

# create a cursor
cur = conn.cursor()


def consumer_event(topic_name: str):
    """
    Event consumer function to receive data from Kafka topic
    :param topic_name:
    :return:
    """
    consumer = KafkaConsumer(topic_name, bootstrap_servers=f'{KAFKA_HOST}:{KAFKA_PORT}',
                             auto_offset_reset='earliest', enable_auto_commit=True)
    for msg in consumer:
        event = json.loads(msg.value.decode('utf-8'))
        str_date_time = event['date_time']
        date_time = datetime.datetime(int(str_date_time[0:4]), int(str_date_time[5:7]), int(str_date_time[8:10]),
                                      int(str_date_time[11:13]), int(str_date_time[14:16]), int(str_date_time[17:19]),
                                      tzinfo=pytz.timezone('Europe/Paris'))
        # query = """
        #     INSERT INTO events (name, description, date_time)
        #     VALUES (%s, %s, %s);
        # """
        # cur.execute(query, (event['name'], event['description'], date_time))
        # conn.commit()
        print(event)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    consumer_event("weather-data-pipeline")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
