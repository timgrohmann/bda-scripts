import kafka
import requests
import json

producer = kafka.KafkaProducer()

print('http request ...')
json_data = requests.get(url='https://api.covid19api.com/dayone/country/germany/status/confirmed').json()

print('Response: ', len(json_data), ' entities')

count = 0
for i, line in enumerate(json_data):
    count += 1
    print('sending message, #', count)
    producer.send('corona-http', value=bytearray(json.dumps(line), encoding='utf-8'), key=bytearray(str(i), encoding='utf-8'))

