from paho.mqtt.client import *
from paho import mqtt
import json

#------ DATA -------
broker = '9fe9cc9c581f455dbb228c6a907ae1e3.s1.eu.hivemq.cloud'
port_broker = 8883
topic = 'home/satnza1/temperatura'
keep_alive = 60

# ----- FUNZIONI ---

def on_message(client, userdata, msg):
    data_json = msg.payload.decode("utf-8")
    print(data_json)
    print('---------------------------')

# ---- MAIN --------

# creazione istanza clinet
client = Client()

#callback
client.on_message = on_message

client.tls_set(tls_version= mqtt.client.ssl.PROTOCOL_TLS)

#username e password
client.username_pw_set("trive2004", "beppe100204")

# conessione con del client con il broker
client.connect(broker, port_broker, keep_alive)

client.subscribe(topic)

try:
    while(True):
        client.loop_forever()
        
except KeyboardInterrupt:
    print('stop subscriber')

