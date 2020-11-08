(Platzhalter Deckblatt, TOC)

## 1. Aufgabenstellung

## 2. Datenquellen

### 2.1. Passantenfrequenzen

### 2.2. Coronafallzahlen

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

### 3.2. Importieren der Daten in die Datenbank mit Kafka

### 3.3. Transformation der Daten

### 3.4. Auswertung

## Probleme / Lösungen

## Fazit