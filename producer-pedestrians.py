import kafka

producer = kafka.KafkaProducer()

paths = [
    'data/frankfurt a.m.-goethestraße-20180930-20201031-day.csv',
    'data/stuttgart-königstraße (mitte)-20180930-20201031-day.csv',
    'data/düsseldorf-königsallee ostseite (süd)-20180930-20201031-day.csv',
    'data/frankfurt a.m.-große bockenheimer straße-20180930-20201031-day.csv'
]

for path in paths:
    dataset = open(path, encoding='utf-8')
    lines = dataset.readlines()[1:]

    for i, line in enumerate(lines):
        print(line)
        producer.send('peoplecount', value=bytearray(line, encoding='utf-8'))
