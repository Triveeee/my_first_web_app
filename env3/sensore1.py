from paho.mqtt.client import *
from paho import mqtt
import json
from time import *
import random

#------ DATA -------
broker = '9fe9cc9c581f455dbb228c6a907ae1e3.s1.eu.hivemq.cloud'
port_broker = 8883
topic = 'home/satnza1/temperatura'
keep_alive = 60

# ----- FUNCTION ----
def createRoom():
    temp = random.randrange(10,30)
    umidita = random.randint(0,40)
    return {
        "temp": temp,
        "umidita": umidita,
        "stanza": "stanza_1"
    }

# ------ MAIN -------

#istanza client
client = Client()


client.tls_set(tls_version= mqtt.client.ssl.PROTOCOL_TLS)

#username e password
client.username_pw_set("trive2004", "beppe100204")

#conessione al broker
client.connect(broker,port_broker,keep_alive)


#invio dati
client.loop_start()
try:
    while(True):
        stanza = createRoom()
        data_json = json.dumps(stanza, indent=4)
        print(data_json)
        client.publish(topic, data_json)   # <--- [pubblicazione dati]
        sleep(5)
except KeyboardInterrupt:
    print('stop publisher')

client.loop_stop()

#disconessione client
client.disconnect()

# ------ FINE_MAIN ------






