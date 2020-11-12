import kafka
import datetime as dt
from pymongo import MongoClient

# Verbindung mit Kafka für Topic 'peoplecount'
consumer = kafka.KafkaConsumer('peoplecount')

# Verbindung mit Mongo-Server für Collection 'peoplecount'
client = MongoClient()
pp = client['bigdata']['peoplecount']

# Löschen bereits vorhandener Daten, damit keine Duplikate beim mehrfachen Ausführen entstehen
pp.delete_many({})

# Initialisieren eines leeren Dictionairies, in das später Werte für moving average abgelegt werden
sums = {}

for message in consumer:
    values = message.value.decode('utf-8').split(';')
    place = values[0]

    count = int(values[3])
    if count == 0:
        if place not in sums:
            continue
        else:
            val = sums[place]
            # calculate moving average
            count = round(float(val['total'])/val['count'])
    else:
        if place not in sums:
            sums[place] = {'count': 1, 'total': count}
        else:
            sums[place]['count'] += 1
            sums[place]['total'] += count

    pp.insert_one({
        'day': dt.datetime.strptime(values[1][:-6],"%Y-%m-%d %H:%M:%S"),
        'count': count,
    })
    