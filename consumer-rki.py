import kafka
from pymongo import MongoClient
import csv
from datetime import datetime

consumer = kafka.KafkaConsumer('rki')

client = MongoClient()
pp = client['bigdata']['corona']

for message in consumer:
    values = list(csv.reader([message.value.decode('utf-8')], delimiter=','))[0]

    # print(values)
    try:
        pp.insert_one({
            'IdBundesland': int(values[0]),
            'Bundesland': values[1],
            'Landkreis': values[2],
            'Altersgruppe': values[3],
            'Geschlecht': values[4],
            'AnzahlFall': int(values[5]),
            'AnzahlTodesfall': int(values[6]),
            'ObjectId': values[7],
            'IdLandkreis': values[8],
            'Altersgruppe2': values[9],
            'Refdatum': datetime.fromtimestamp(int(values[10]) // 1000),
            'Meldedatum': datetime.fromtimestamp(int(values[11]) // 1000),
            'IstErkrankungsbeginn': int(values[12]),
            'NeuerFall': int(values[13]),
            'NeuerTodesfall': int(values[14]),
            'NeuGenesen': (values[15]),
            'AnzahlGenesen': int(values[16]),
            'Datenstand': values[17]
        })
    except Exception as e:
        print(e)
        print(values)