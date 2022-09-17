from machine import UART
from time import sleep
from mqtt import MQTTClient
import json

#Change Me
mqtt_uid = "Gateway-1"
mqtt_user = "zone2"
mqtt_pass = "changeme"
mqtt_server = "ip or domain.com"
mqtt_port = "1883"

uart_tx =16
uart_rx = 17
uart_baudrate = 115200

sta_ssid = "WiFiChangeMe-2.4G"
sta_pass = "changeme"

nodes = ['Node_1', 'Node_2', 'Node_3', 'Node_4', 'Node_5']
zones = ['1']
###########################################
uart1 = UART(2, baudrate=115200, tx=uart_tx, rx=uart_rx)
print('Initilazing..')
sleep(5)

client = MQTTClient(mqtt_uid, mqtt_server, user=mqtt_user, password=mqtt_pass, port=mqtt_port)

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
for i in zones:
    z = i
    for i in nodes:
        n = i
        client.subscribe(topic='Zone{0}/{1}'.format(z,n))
        
while True:
    uartmsg = uart1.read()
    if uartmsg is None:
        pass
    else:
        get_nodes = json.loads(uartmsg.decode('utf-8')).values()
        for n in nodes:
            if n in get_nodes:
                node = uartmsg.decode('utf-8')
                #print(node)
                for z in zones:
                    if z in node:
                        client.publish(topic='Zone{0}/{1}'.format(z,n), msg=node, qos=1)
