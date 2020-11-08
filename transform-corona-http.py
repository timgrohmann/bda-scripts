from pymongo import MongoClient
import datetime as dt

client = MongoClient()
rawDataCollection = client['bigdata']['corona-deutschland']

newDataCollection = client['bigdata']['corona-deutschland-neue-faelle']

for value in rawDataCollection.find():
    previousDay = rawDataCollection.find_one({ 'Date': (value['Date'] - dt.timedelta(days = 1)) })

    if (previousDay is None):
        value['neueFaelle'] = None
    else:
        value['neueFaelle'] = value['Cases'] - previousDay['Cases']

    newDataCollection.insert_one(value)
