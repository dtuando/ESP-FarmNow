from machine import UART
from time import sleep
from mqtt import MQTTClient
import json


#Change Me
mqtt_uid = ""
mqtt_user = ""
mqtt_pass = ""
mqtt_server = ""
mqtt_port = "1883"

node_1_topic = ""
node_2_topic = ""
node_3_topic = ""
node_4_topic = ""

uart_tx =16
uart_rx = 17
uart_baudrate = 115200

sta_ssid = ""
sta_pass = ""
###########################################
uart1 = UART(2, baudrate=uart_baudrate, tx=uart_tx, rx=uart_rx)
print('Initilazing..')
sleep(5)

nodes = []
node_1 = ""
node_2 = ""
node_3 = ""
node_4 = ""

client = MQTTClient(mqtt_uid, mqtt_server,user=mqtt_user, password=mqtt_pass, port=mqtt_port)

def sub_cb(topic, msg):
   print(msg)
   
def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(sta_ssid, sta_pass)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
    
do_connect()
client.set_callback(sub_cb)
client.connect()
client.subscribe(topic=node_1_topic)
client.subscribe(topic=node_2_topic)
client.subscribe(topic=node_3_topic)
client.subscribe(topic=node_4_topic)
while True:
    uartmsg = uart1.read()
    if uartmsg is None:
        pass
    else:
        nodes = json.loads(uartmsg.decode('utf-8')).values()
        if 'Node_1' in nodes:
            node_1 = uartmsg.decode('utf-8')
            #print(json.loads(uartmsg.decode('utf-8')))
            client.publish(topic=node_1_topic, msg=node_1, qos=1)
        if 'Node_2' in nodes:
            node_2 = uartmsg.decode('utf-8')
            #print(json.loads(uartmsg.decode('utf-8')))
            client.publish(topic=node_2_topic, msg=node_2, qos=1)
        if 'Node_3' in nodes:
            node_3 = uartmsg.decode('utf-8')
            #print(json.loads(uartmsg.decode('utf-8')))
            client.publish(topic=node_3_topic, msg=node_3, qos=1)
        if 'Node_4' in nodes:
            node_4 = uartmsg.decode('utf-8')
            print(json.loads(uartmsg.decode('utf-8')))
            client.publish(topic=node_4_topic, msg=node_4, qos=1)
