# Proiect IoT
# Se preiau datele de la un WazeAPI, se salveaza intr-un fisier .json local si in cloud prin intermediul S3 AWS,
# se trimite un SMS cand un parametrul severity depaseste pragul 3.

# Importare pachete.

from datetime import datetime
from twilio.rest import Client
import json
import requests
import os
import boto3

# Configurari fisier .json

url = "https://waze.p.rapidapi.com/alerts-and-jams"     # setare URL api
currentTime = datetime.now().strftime("%H-%M-%S")       # preluare ora curenta
outputFile = f"waze_data_{currentTime}.json"            # setare nume fisier json in functie de ora curenta

# Configurari trimitere date in cloud (AWS S3).

client = boto3.client('s3')
bucketName = 's3-bucket-iotproject'                     # numele bucket-ului creat in S3 AWS

curPath = os.getcwd()
file = f"waze_data_{currentTime}.json"
filename = os.path.join(curPath, file)                  # path-ul fisierului .json

# Configurari notificare SMS (Twilio).

account_sid = '--'
auth_token = '--'
clientMsg = Client(account_sid, auth_token)

# Introducere numar de ambuteiaje.

val_jams = input("Enter the number of jams:")

# Waze API Call.

querystring = {
    "bottom_left": "46.735776, 23.710680",                 # setare coordonate
    "top_right": "46.798600, 23.537560",
    "max_jams": val_jams}                                  # setare numar maxim de alerte

headers = {
    "X-RapidAPI-Key": "--",       # API key
    "X-RapidAPI-Host": "waze.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

# Extragere date de la API.

if response.status_code == 200:
    data = response.json()                 # preluare date

    # Extragere si printare a parametrilor fiecarei alerte.

    jams = data["data"]["jams"]
    jamsData = []

    for jam in jams:
        severity = jam["severity"]
        speed_kmh = jam["speed_kmh"]
        publish_datetime_utc = jam["publish_datetime_utc"]
        city = jam["city"]
        street = jam["street"]

        print("severity:", severity)
        print("speedkmh:", speed_kmh)
        print("City:", city)                       # afisarea parametrilor in consola
        print("Street:", street)
        print("Publish date:", publish_datetime_utc)

        # Daca severitatea unei alerte este mai mare ca 3, se trimite un SMS de notificare.

        #*if severity > 3:
            #message = clientMsg.messages.create(
               # from_='+12513331854',
              #  body='Severity is greater than 3!',
             #   to='+40751547360'
            #)

        # Salvarea datelor in fisierul .json

        jamsData.append({
            "Severity:": severity,
            "Speed": speed_kmh,
            "City": city,
            "Street": street,
            "Publish Date": publish_datetime_utc
        })

        with open(outputFile, "w", encoding='utf8') as json_file:               # deschidere fisier .json
            json.dump(jamsData, json_file, indent=4, ensure_ascii=False)        # scriere in fisier
else:
    print("Failed to retrieve data. Status code:", response.status_code)

# Trimitere date in cloud (AWS S3).

date = open(filename, 'rb')
client.upload_file(filename, bucketName, file)
