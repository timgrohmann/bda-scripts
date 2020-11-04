import kafka
import datetime as dt
from pymongo import MongoClient

consumer = kafka.KafkaConsumer('peoplecount')

client = MongoClient()
pp = client['bigdata']['peoplecount']
pp.delete_many({})

for message in consumer:
    print('inserting new message')
    values = message.value.decode('utf-8').split(';')
    pp.insert_one({
        'place': values[0],
        'day': dt.datetime.strptime(values[1][:-6],"%Y-%m-%d %H:%M:%S"),
        'weekday': values[2],
        'count': int(values[3]),
        'temp': int(values[4]) if values[4] != '' else None,
        'weather': values[5],
    })
    