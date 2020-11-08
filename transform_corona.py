from pymongo import MongoClient
from pprint import pprint

client = MongoClient()
rawDataCollection = client['bigdata']['corona']

newDataCollection = client['bigdata']['neueFaelleByLandkreis']

pipeline = [
    {
        '$group': {
            '_id': {
                'Landkreis': '$Landkreis', 
                'Meldedatum': '$Meldedatum'
            }, 
            'NeueFaelle': {
                '$sum': '$AnzahlFall'
            }
        }
    }, {
        '$project': {
            '_id': 0, 
            'Landkreis': '$_id.Landkreis', 
            'Meldedatum': '$_id.Meldedatum', 
            'NeueFaelle': 1
        }
    }
]

for value in rawDataCollection.aggregate(pipeline):
  newDataCollection.insert_one(value)
