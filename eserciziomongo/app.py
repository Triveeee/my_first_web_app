from pymongo import * 
from paho.mqtt.client import *
from random import *
from datetime import *
from time import *
from json import *
import utils.index as utils

#------------------------------------------------
#Dati

topic = 'atlas/mongodb/case'
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
def stream(n_casa):
    try:
        while(True):
            utils.clear()
            dati = collection.find({"payload.casa": n_casa})
            serie = utils.createSeries(dati)
            print(serie)
            sleep(5)
    except KeyboardInterrupt:
        print('stop')

def media(n_casa):
    try : 
        while(True):
            utils.clear()
            dati = collection.find({"payload.casa": n_casa})
            dati = list(dati)
            dati = utils.findLastElement(dati , 5)
            utils.show()
            sleep(2)
    except KeyboardInterrupt:
        print('stop')

def on_message(client , userdata , msg):
    dati_json = msg.payload.decode("utf-8")
    print(dati_json)

#---------------------------------------------
#CallBack
client.on_message = on_message

#---------------------------------------------
#Main
item = utils.menu()
client.subscribe(item[0])

if(item[1] == 1):
    stream(item[2])
if(item[1] == 2):
    media(item[2])


