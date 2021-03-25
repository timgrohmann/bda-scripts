import datetime as dt
from pymongo import MongoClient


# Verbindung mit Mongo-Server für Collection 'peoplecount'
client = MongoClient()
pp = client['bigdata']['peoplecount']
pp.delete_many({})

# Initialisieren eines leeren Dictionairies, in das später Werte für moving average abgelegt werden
sums = {}

paths = [
    'data/frankfurt a.m.-goethestraße-20180930-20210325-day.csv',
    'data/stuttgart-königstraße (mitte)-20180930-20210325-day.csv',
    'data/düsseldorf-königsallee ostseite (süd)-20180930-20210325-day.csv',
    'data/frankfurt a.m.-große bockenheimer straße-20180930-20210325-day.csv'
]

for path in paths:
    dataset = open(path, encoding='utf-8')
    lines = dataset.readlines()[1:]

    for line in lines:
        values = line.split(';')
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