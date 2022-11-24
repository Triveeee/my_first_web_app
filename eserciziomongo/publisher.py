from pymongo import * 
from paho.mqtt.client import *
from random import *
from datetime import *
from time import *
import json

#------------------------------------------------
#Dati

topic = 'casa/1/misurazioni'
BROKER_HOST = '80.210.122.173'
PORTA_BROKER = 1883


#-----------------------------------------------
#Conessione al broker

client = Client()
client.connect(BROKER_HOST,PORTA_BROKER)


#-----------------------------------------------
#Conessione ad Atlas

password = 'trive004'
uri = 'mongodb+srv://riccardo:'+ password + '@cluster0.zzvi9yy.mongodb.net/test'
atlas = MongoClient(uri)
db = atlas.cluster0
collection = db.case

#----------------------------------------------
#Funzioni

def createHome(n_casa):
    temp = randint(0,40)
    umidita = randint(1 , 100)
    time_stamp = datetime.now
    home = {
        "casa": n_casa,
        "tempo": str(time_stamp),
        "stanze": [
            {"cucina": {"temperatura": temp, "umidita": umidita}},
            {"soggiorno": {"temperatura": temp, "umidita": umidita}},
            {"mansarda": {"temperatura": temp, "umidita": umidita}},
            {"camera_da_letto": {"temperatura": temp, "umidita": umidita}}
        ]
    }
    home = json.dumps(home , indent=4)
    return home

#--------------------------------------------
#Main

client.loop_start()

try:
    while True:
        casa = createHome(1)
        print(casa)
        client.publish(topic, casa)
        sleep(5)

except KeyboardInterrupt:
    print("Stop publisher")
client.loop_stop()
client.disconnect()








