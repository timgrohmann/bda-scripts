import kafka

producer = kafka.KafkaProducer()

dataset = open('data/frankfurt a.m.-goethestraße-20180930-20201031-day.csv', encoding='utf-8')
lines = dataset.readlines()[1:]

for i, line in enumerate(lines):
    print(line)
    producer.send('peoplecount', value=bytearray(line, encoding='utf-8'), key=bytearray(str(i), encoding='utf-8'))
