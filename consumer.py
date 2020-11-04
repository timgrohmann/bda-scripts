import kafka
from pymongo import MongoClient

consumer = kafka.KafkaConsumer('peoplecount')

client = MongoClient()
pp = client['bigdata']['peoplecount']

for message in consumer:
    print('inserting new message')
    values = message.value.decode('utf-8').split(';')
    pp.insert_one({
        'place': values[0],
        'timestamp': values[1],
        'weekday': values[2],
        'count': values[3],
        'temp': values[4],
        'weather': values[5],
    })
    