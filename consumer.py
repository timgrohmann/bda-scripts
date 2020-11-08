import kafka
import datetime as dt
from pymongo import MongoClient

consumer = kafka.KafkaConsumer('peoplecount')

client = MongoClient()
pp = client['bigdata']['peoplecount']
pp.delete_many({})

sums = {}

for message in consumer:
    print('inserting new message')
    values = message.value.decode('utf-8').split(';')
    place = values[0]
    count = int(values[3])
    if count == 0:
        if place not in sums:
            continue
        else:
            val = sums[place]
            count = round(float(val['total'])/val['count'])
    else:
        if place not in sums:
            sums[place] = {'count': 1, 'total': count}
        else:
            sums[place]['count'] += 1
            sums[place]['total'] += count
    pp.insert_one({
        'place': place,
        'day': dt.datetime.strptime(values[1][:-6],"%Y-%m-%d %H:%M:%S"),
        'weekday': values[2],
        'count': count,
        'temp': int(values[4]) if values[4] != '' else None,
        'weather': values[5],
    })
    