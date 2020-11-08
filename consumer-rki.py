import kafka
from pymongo import MongoClient
import csv
from datetime import datetime

# docker run -p 27017:27017 -v 

consumer = kafka.KafkaConsumer('rki')

client = MongoClient()
pp = client['bigdata']['corona']

for message in consumer:
    values = list(csv.reader([message.value.decode('utf-8')], delimiter=','))[0]

    # print(values)
    try:
        neuerFall = int(values[11])

        if (neuerFall == 1):
            pp.insert_one({
                'FID': values[0],
                'IdBundesland': int(values[1]),
                'Bundesland': values[2],
                'Landkreis': values[3],
                'Altersgruppe': values[4],
                'Geschlecht': values[5],
                'AnzahlFall': int(values[6]),
                'AnzahlTodesfall': int(values[7]),
                'Meldedatum': datetime.strptime(values[8], '%Y/%m/%d %H:%M:%S'),
                'IdLandkreis': values[9],
                'Datenstand': values[10],
                'NeuerFall': neuerFall,
                'NeuerTodesfall': int(values[12]),
                'Refdatum':datetime.strptime(values[13], '%Y/%m/%d %H:%M:%S'),
                'NeuGenesen': (values[14]),
                'AnzahlGenesen': int(values[15]),
                'IstErkrankungsbeginn': int(values[16]),
                'Altersgruppe2': values[17]
            })
    except Exception as e:
        print(e)
        print(values)