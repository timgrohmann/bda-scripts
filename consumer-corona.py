import kafka
from pymongo import MongoClient
import json
from datetime import datetime

consumer = kafka.KafkaConsumer('corona')

client = MongoClient()
pp = client['bigdata']['corona-deutschland']

count = 0

for message in consumer:
    count += 1
    print('Got new message: #', count)
    values = json.loads(message.value.decode('utf-8'))
    try:
        pp.insert_one({
            'Country': values['Country'],
            'CountryCode': values['CountryCode'],
            'Cases': values['Cases'],
            'Status': values['Status'],
            'Date': datetime.strptime(values['Date'], '%Y-%m-%dT%H:%M:%SZ'),
        })
    except Exception as e:
        print(e)
        print(values)