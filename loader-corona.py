import requests
import json
from pymongo import MongoClient
from datetime import datetime


print('http request ...')
json_data = requests.get(url='https://api.covid19api.com/dayone/country/germany/status/confirmed').json()

print('Response: ', len(json_data), ' entities')

client = MongoClient()
collection = client['bigdata']['corona-deutschland']
collection.delete_many({})

for line in json_data:
    values = line
    try:
        collection.insert_one({
            'Country': values['Country'],
            'CountryCode': values['CountryCode'],
            'Cases': values['Cases'],
            'Status': values['Status'],
            'Date': datetime.strptime(values['Date'], '%Y-%m-%dT%H:%M:%SZ'),
        })
    except Exception as e:
        print(e)
        print(values)

