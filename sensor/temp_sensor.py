import network, ubinascii, espnow, onewire, time, ds18x20, json
from machine import Pin, deepsleep
from time import sleep, sleep_ms


#CHANGE THESE SETTINGS
zone = "1"
uid = "Node_1"
temp =  ""
gateways = [b'\xaa\xaa\xaa\xaa\xaa\xaa']
tempsensor = Pin(14)

#Advanced Settings
ow = onewire.OneWire(tempsensor)
ds = ds18x20.DS18X20(ow)
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.config(protocol=network.MODE_LR)
e = espnow.ESPNow()
e.active(True)

#functions
def get_data(uid,temp):
    node = {}
    node["Zone"] = zone
    node["ID"] = uid
    node["Temperature"] = temp
    return node

def get_temp():
    roms = ds.scan()
    ds.convert_temp()
    sleep_ms(750)
    for rom in roms:
        temp = ds.read_temp(rom) * 1.8 + 32
    return temp

def send_temp():
    for i in gateways:
        e.send(i, json.dumps(get_data(uid,get_temp())))
        sleep(1)
        
def irq_cb(code, data):
    if code == espnow.EVENT_RECV_MSG:
        peer, msg = data
        if msg.decode('utf-8') == 'temp':
            print(json.dumps(get_data(uid,get_temp())))
            send_temp()
        elif 'sleep' in msg.decode('utf-8'):
            e.active(False)
            sta.active(False)                 # Disable the wifi before sleep
            print('Going to sleep...')
            sleep(3)
            deepsleep(25000)   

#initilize
mac = ubinascii.hexlify(network.WLAN(network.STA_IF).config('mac'),':').decode()
print("MAC: " + mac)
for i in gateways:
    e.add_peer(i)
    
e.irq(irq_cb)