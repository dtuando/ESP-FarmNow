import network, ubinascii
import espnow
from time import sleep
from machine import UART, deepsleep

uart_tx = 17
uart_rx = 16
uid = 'GW-2'

uart1 = UART(2, baudrate=115200, tx=uart_tx, rx=uart_rx)

mqtt_msg = []
# A WLAN interface must be active to send()/recv()
network.WLAN(network.STA_IF).active(True)

mac = ubinascii.hexlify(network.WLAN(network.STA_IF).config('mac'),':').decode()
print("MAC: " + mac)

e = espnow.ESPNow()  # Returns AIOESPNow enhanced with async support
e.active(True)
bcast = b'\xff' * 6
e.add_peer(bcast)

def recv_cb(e):
    host, msg = e.irecv(0)
    if msg:
        payload = msg.decode('utf-8')
        mqtt_msg.append(msg.decode('utf-8'))
        print(payload)
        send_to_top()
          
def send_to_top():
    for i in mqtt_msg:
        uart1.write(i)
    sleep(1)
    mqtt_msg.clear()
    
    
########################################

print('Initializing...')
sleep(5)

e.on_recv(recv_cb, e)

