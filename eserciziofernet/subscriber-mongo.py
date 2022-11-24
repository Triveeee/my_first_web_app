from pymongo import * 
from paho.mqtt.client import *
from random import *
from datetime import *
from cryptography.fernet import Fernet
from time import *
from json import *

#------------------------------------------------
#Dati
chiave = 'fM5t5hPaMlRWtmfpnbaaDAsYJvsDnDE5Ehd_9oYirEg='
topic = 'casa/1/misurazioni'
BROKER_HOST = '80.210.122.173'
PORTA_BROKER = 1883

#---------------------------------------------
# definizione chiave

chiave = 'fM5t5hPaMlRWtmfpnbaaDAsYJvsDnDE5Ehd_9oYirEg='
chiave_valore = Fernet(chiave)

#-----------------------------------------------
#Conessione ad Atlas

password = 'trive004'
uri = 'mongodb+srv://riccardo:'+ password + '@cluster0.zzvi9yy.mongodb.net/test'
atlas = MongoClient(uri)
db = atlas.cluster0
collection = db.case

#-----------------------------------------------
#Conessione al broker

client = Client()
client.connect(BROKER_HOST,PORTA_BROKER)

#----------------------------------------------
#Funzioni

#trova l'indice di partenza
def findLastIndex():
    id_msg = 1
    res = collection.find_one({'_id': id_msg})
    if(res != None):
        while(res != None):
            id_msg+=1
            res = collection.find_one({'_id': id_msg})
    return(id_msg)

def on_message(client , userdata , msg):
    id_msg = findLastIndex()  # <--- richiama la funzione findlastindex
    message_cryptated = msg.payload.decode("utf-8")  # <--- decodificazione del messaggio inviato dal broher (bytes criptato -> string criptato)
    message_bytes = chiave_valore.decrypt(message_cryptated) # <--- decriptazione del messaggio in bytes (string criptato-> bytes decriptato) 
    message_json = message_bytes.decode("utf-8") # <-- decodifica del messaggio decriptato in bytes  (bytes decriptato -> string decriptato)
    message_cryptated = {"_id": id_msg, "payload": message_cryptated} # <-- conversione in un dizionario in modo da agiungerlo nel database (mesaggio criptato)
    collection.insert_one(message_cryptated)
    print(message_json) # <-- visualizzazione del messaggio in chiaro

#---------------------------------------------
#CallBack
client.on_message = on_message

#---------------------------------------------
#Main
client.subscribe(topic)
try:
    client.loop_forever()
except KeyboardInterrupt:
    print("stop_subscriber")
