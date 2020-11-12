(Platzhalter Deckblatt, TOC)

## 1. Aufgabenstellung

*von Niclas Kaufmann*

## 2. Datenquellen

In dem Projekt werden insgesamt zwei Datenquellen verwendet, welche im Folgenden näher erläutert werden sollen.

### 2.1. Passantenfrequenzen

*von Tim Grohmann*

Daten über die Passentenfrequenzen in Deutschen Innenstädten werden von *hystreet.com*, einer Initiative der Aachener Grundvermögen, erhoben und sind bis zu stundengenau frei von ebendieser Website als CSV-Dateien herunterladbar.

Für dieses Projekt war ein großer Abdeckungszeitraum der Datenquellen wichtig, da der Zeitraum von Oktober 2018 - September 2019 mit dem Zeitraum Oktober 2019 - Septeber 2020 verglichen wird.
Deshalb kommen viele Messpunkte von *hystreet* nicht in Frage, da diese erst nach Oktober 2018 installiert wurden.
Um ein möglichst aussagekräftiges Ergebnis zu erhalten, wurden für die Auswertung 4 Messpunkte miteineander kombiniert:

- Frankfurt/M, Goethestraße
- Frankfurt/M, Große Bockenheimer Straße
- Düsseldorf, KÖ
- Stuttgart, Königstraße

So soll verhindert werden, das einzelne lokale Ereignisse (Demonstation, Stadtfest, etc.) zu großen Ausreißern in den Daten führen.

Da die Fluktuation von Passantenzahlen während eines Tages für diese Betrachtung irrelevant sind, wurden nur tagesgenaue CSVs von hystreet exportiert. Die Datensätze in diesen CSV-Dateien sind wie folgt strukturiert.

| Spalte                  | Bedeutung                                                      |
| ----------------------- | -------------------------------------------------------------- |
| **location**            | Standort der Messung, in einer Datei jeweils gleich            |
| **time of measurement** | Zeitpunkt der Messung, jeweils 00.00 Uhr des betroffenen Tages |
| weekday                 | Wochentag der Messung                                          |
| **pedestrians count**   | Anzahl der Fußgänger an diesem Tag                             |
| temperature in ºc       | Temperatur im Messzeitraum                                     |
| weather condition       | Wetterverhältnisse im Messzeitraum                             |
| incidents               | besondere Vorkommnisse (Sensorausfall o.ä.)                    |

Die für diese Auswertung relevanten Spalten wurden **fett** markiert.

### 2.2. Coronafallzahlen

*von Niclas Kaufmann*

Die täglichen Corona-Fallzahlen für Deutschland werden von der COVID 19 API (https://covid19api.com/) bereitgestellt. Diese Daten stammen von dem Coronavirus Resource Center der Johns Hopkins Univerity in Maryland.

Die API unterstützt verschiedene Endpunkte, um Daten zu den Fallzahlen abzufragen. Die kostenlose Variante benötigt keinen API-Schlüssel, um auf die Daten zuzugreifen. Für das Projekt wird der Endpunkt `/dayone/country/:country/status/confirmed` verwendet. Dieser Endpunkt gibt für jeden Tag nach der ersten Aufzeichnung die Fallzahlen zurück, die bestätigt sind. Für Deutschland (`country := 'germany'`) werden also alle Tage, ab dem 27. Januar 2020 zurückgegeben.

Zurückgegeben wird ein JSON-Array, welches für jeden Tag ein Objekt mit folgendem Schema enthält:
```json
  {
    "Country": "string",
    "CountryCode": "string",
    "Province": "string",
    "City": "string",
    "CityCode": "string",
    "Lat": "string",
    "Lon": "string",
    "Cases": "number",
    "Status": "string",
    "Date": "string"
  }
```
Für Deutschland sind die Eigenschaften von `Province`, `City` und `CityCode` nicht ausgefüllt, bzw. ein leerer String, da die Daten für ganz Deutschland abgefragt werden und nicht für einzelne Städte oder Bundesländer. Die `Cases` sind die summierten Fallzahlen für das jeweilige Land, unabhängig, ob der Mensch das Virus überwunden hat oder nicht. Das Attribut `Date` ist ein UTC-konformer String.

Als Beispiel soll das Objekt für den 22. Juli 2020 (generiert am 05. November 2020) gezeigt werden:
```json
  {
      "Country": "Germany",
      "CountryCode": "DE",
      "Province": "",
      "City": "",
      "CityCode": "",
      "Lat": "51.17",
      "Lon": "10.45",
      "Cases": 204276,
      "Status": "confirmed",
      "Date": "2020-07-22T00:00:00Z"
  }
```


## 3. Umsetzung

### 3.1. Verwendete Technologien
*von Niclas Kaufmann*

### 3.2. Importieren der Daten in die Datenbank mit Kafka
*von Niclas Kaufmann*

Die Datenquellen (beschrieben in Kapitel 2) werden mit Hilfe von Kafka in die Datenbank geladen. Zuerst lädt der Producer die Datenquelle und sendet die einzelnen Daten an ein bestimmtes Topic des Kafka Senders. Der Consumer abboniert auf dieses Topic. Wichtig ist, dass der Consumer nur Nachrichten des Producers beachtet, die nach dem Abonnement gesendet werden.
Die verschiedenen Producer und Consumer für die Passantenfrequenzen und Corona-Fallzahlen werden im Folgenden beschrieben.

#### **Producer für Passantenfrequenzen**
*von Tim Grohmann*

Die Passentenfrequenzen werden aus mehreren CSV-Dateien ausgelesen, deren relative Dateipfade in einem Array angegeben werden können.
Aus jeder dieser Datei wird nun Zeile für Zeile gelesen (die Kopfzeile muss dabei übersprungen werden) und der Inhalt jeder Zeile als UTF-8-kodierter String an das Kafka-Topic `peoplecount` gesendet.

#### **Consumer für Passantenfrequenzen**
*von Tim Grohmann*

Im entsprechenden Consumer werden diese Daten wieder zurück in einen String konvertiert und nach dem Trennzeichen `;` aufgesplittet. Eine einzelne Zeile aus der CSV-Datei ist jetzt also als Array von Strings vorhanden.

In den Datensätzen sind einige Tage vorhanden, an denen 0 Fußgänger gezählt werden. Das ist äußerst unwahrscheinlich und demzufolge auf eine Systemstörung zurückzuführen.
Damit diese fehlerhaften Datensätze die Analyse nicht verfälschen, werden sie im Consumer mit dem *moving average* des jeweiligen Standortes aufgefüllt.
Dazu werden in einem Dictionary `sums` mit dem Namen des Standorts als Schlüssel ein weiteres Dictionary abgelegt, das zum einen die Menge gezählter Tage (`count`) und zum anderen die kumulative Personenzahl (`total`) enthält.
Sollte im Consumer nun ein Datensatz mit einer vemeintlichen Personenzahl von 0 gelesen, wird nicht diese 0 in die Datenbank geschrieben, sondern der bisherige Durchschnitt `total / count`.

#### **Producer für Corona-Fallzahlen**
*von Niclas Kaufmann*

Der Producer für die Corona-Fallzahlen ist in der Python-Datei `producer-corona.py` implentiert und hat den folgenden Aufbau (die Print-Befehle wurden der Übersichthalber entfernt): 

```python
import kafka
import requests
import json

json_data = requests.get(url='https://api.covid19api.com/dayone/country/germany/status/confirmed').json()

producer = kafka.KafkaProducer()

for i, line in enumerate(json_data):
    producer.send('corona', value=bytearray(json.dumps(line), encoding='utf-8'), key=bytearray(str(i), encoding='utf-8'))
```

Zu erst wird ein HTTP-Request an die COVID 19 API gestellt, der sich die Corona-Fallzahlen abfragt. Als nächstes wird ein Producer initialisiert. Da der Kafka-Server auf der Standard-Adresse `localhost:9092` läuft, muss sie nicht weiter angegeben werden. Der Producer sendet für jedes Objekt des JSON-Arrays einen geparsten String an das Topic `corona`.

#### **Consumer für Corona-Fallzahlen**
*von Niclas Kaufmann*

In der Datei `consumer-corona.py` wird der Consumer für die Corona-Fallzahlen implementiert. Im Folgenden wird der Inhalt der Datei gezeigt (die Print-Befehle wurden der Übersichthalber entfernt):

```py
import kafka
from pymongo import MongoClient
import json
from datetime import datetime

consumer = kafka.KafkaConsumer('corona')

client = MongoClient()
collection = client['bigdata']['corona-deutschland']

for message in consumer:
    values = json.loads(message.value.decode('utf-8'))
    try:
        collection.insert_one({
            'Country': values['Country'],
            'CountryCode': values['CountryCode'],
            'Cases': values['Cases'],
            'Status': values['Status'],
            'Date': datetime.strptime(values['Date'], '%Y-%m-%dT%H:%M:%SZ'),
        })
    except Exception as e:
        print(e)
        print(values)
```

Als erstes wird der Consumer auf das Topic `corona` und die MongoDB-Datenbank initialisiert. Die Kollektion, in der die Daten gespeichert werden sollen, ist `bigdata.corona-deutschland`.

Nun wird für jede Nachricht, die der Consumer empfängt, folgendes getan: Als erstes wird die Nachricht zu einem JSON-Objekt geparst. Nun wird versucht, das geparste Objekt in die Datenbank einzufügen. Bis auf das Attribut `Date` sind alle Attribute Strings, müssen also nicht weiter verändert werden. `Date` wird als Datumsobjekt in die Datenbank eingefügt. Falls ein Fehler auftritt, wird der Fehler sowie das geparste Objekt ausgegeben.

Der Consumer hat eine unendliche Laufzeit, da er ja nicht weiß, wann die letzte Nachricht ankam. Daher muss der Prozess manuell beendet werden.

### 3.3. Transformation der Corona-Fallzahlen

*von Niclas Kaufmann*

Die COVID 19 API gibt die Corona-Fallzahlen nur als kummulierte Werte zurück gibt, für das Projekt werden  aber die täglichen, neuen Fallzahlen benötigt. Daher müssen die Daten transformiert werden. Die Transformation wird in der `transform-corona.py` durchgeführt:

```py
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
```
Es werden die Module `MongoClient` und `Datetime` benötigt. Zu erst wird eine Verbindung zu der MongoDB-Datenbank aufgebaut: Da keine URL angegeben wird, wird die Standard-URL `mongodb://localhost:27017` verwendet. Für jedes Dokument aus der alten Kollektion `bigdata.corona-deutschland` wird das Dokument des Vortages gesucht. Wird kein Vortag gefunden wird an das Dokument des Tages das Attribut `neueFaelle` auf `None` gesetzt und angefügt. Andernfalls berechnet sich `neueFaelle` indem von den Fallzahlen des Tages die Fallzahlen des Vortages abgezogen werden. Zum Schluss wird das Dokument mit dem aktualisierten Attribut in die Kollektion `bigdata.corona-deutschland-neue-faelle` geschrieben.

### 3.4. Auswertung
*von Tim Grohmann*

## Fazit
*von Tim Grohmann*
