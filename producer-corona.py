import kafka
import requests
import json
from pprint import pprint

producer = kafka.KafkaProducer()

print('http request ...')
json_data = requests.get(url='https://api.covid19api.com/dayone/country/germany/status/confirmed').json()

print('Response: ', len(json_data), ' entities')
# dataset = open('data\RKI_COVID19_small.csv', encoding='utf-8')
# dataset = open('data\RKI_COVID19_5_11.csv', encoding='utf-8')
# lines = dataset.readlines()[1:]

count = 0
for i, line in enumerate(json_data):
    count += 1
    print('sending message, #', count)
    producer.send('corona-http', value=bytearray(json.dumps(line), encoding='utf-8'), key=bytearray(str(i), encoding='utf-8'))

