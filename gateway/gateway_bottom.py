import network, ubinascii, espnow
from time import sleep
from machine import UART, deepsleep

uart_tx = 17
aurt_rx = 16
sensors = [b'\xaa\xaa\xaa\xaa\xaa\xaa', b'\xbb\xbb\xbb\xbb\xbb\xbb', b'\xcc\xcc\xcc\xcc\xcc\xcc', b'\xdd\xdd\xdd\xdd\xdd\xdd']


uart1 = UART(2, baudrate=115200, tx=uart_tx, rx=uart_rx)
uid = 'GW-1'

count = 0

mqtt_msg = []
# A WLAN interface must be active to send()/recv()
network.WLAN(network.STA_IF).active(True)

mac = ubinascii.hexlify(network.WLAN(network.STA_IF).config('mac'),':').decode()
print("MAC: " + mac)

e = espnow.ESPNow()  # Returns AIOESPNow enhanced with async support
e.active(True)

for i in sensors:
    e.add_peer(i)

def recv_cb(e):
    host, msg = e.irecv(0)
    if msg:
        mqtt_msg.append(msg.decode('utf-8'))

def check_nodes():
    print('Sending ping...')
    for i in sensors:
        if not e.send(i, b'ping'):
          print('Ping failed!')
        else:
            get_temp()
            sleep(10)
          
def get_temp():
    for i in sensors:
        e.send(i, 'temp')
    sleep(5)
    for i in mqtt_msg:
        uart1.write(i)
        print('Sending mqtt msg: ' + i)
        sleep(1)
    print('Sending Sleep MSG')
    sleep(1)
    for i in sensors:
        e.send(i, 'sleep')
        mqtt_msg.clear()
########################################

print('Initializing...')
sleep(5)

e.on_recv(recv_cb, e)

while True:
    check_nodes()
    sleep(10)
