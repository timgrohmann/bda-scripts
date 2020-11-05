import kafka

producer = kafka.KafkaProducer()

# dataset = open('data\RKI_COVID19_small.csv', encoding='utf-8')
dataset = open('data\RKI_COVID19_5_11.csv', encoding='utf-8')
lines = dataset.readlines()[1:]

for i, line in enumerate(lines):
    producer.send('rki', value=bytearray(line, encoding='utf-8'), key=bytearray(str(i), encoding='utf-8'))

