import network, ubinascii, espnow
from time import sleep
from machine import UART, deepsleep

uart1 = UART(2, baudrate=115200, tx=17, rx=16)
uid = 'GW-1'
sensors = [b'\xaa\xaa\xaa\xaa\xaa\xaa', b'\xbb\xbb\xbb\xbb\xbb\xbb', b'\xcc\xcc\xcc\xcc\xcc\xcc', b'\xdd\xdd\xdd\xdd\xdd\xdd']
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

print('Initializing...')
sleep(5)

e.on_recv(recv_cb, e)

for i in sensors:
    e.send(i, 'temp')

    
sleep(5)
for i in mqtt_msg:
    uart1.write(i)
    print('Sending mqtt msg: ' + i)
    sleep(1)

sleep(1)
print('Sending Sleep MSG')
sleep(1)
for i in sensors:
    e.send(i, 'sleep')

sleep(5)
e.active(False)
print('Going to sleep...')
deepsleep(40000)