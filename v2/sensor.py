import network, ubinascii, espnow, onewire, time, ds18x20, json
from machine import Pin, deepsleep
from time import sleep, sleep_ms


#CHANGE THESE SETTINGS
zone = "1"
uid = "Node_1"
temp =  ""
bcast = b'\xff' * 6
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
    #print(roms)
    ds.convert_temp()
    sleep_ms(750)
    for rom in roms:
        temp = ds.read_temp(rom) * 1.8 + 32
    return temp

def send_temp():
    payload = json.dumps(get_data(uid,get_temp()))
    print('Sending '+ payload)
    e.send(bcast, payload)
    sleep(1)
    
#initilize
mac = ubinascii.hexlify(network.WLAN(network.STA_IF).config('mac'),':').decode()
print("MAC: " + mac)
e.add_peer(bcast)

print('Initializing...')
sleep(5)
while True:
    send_temp()
    sleep(2)
    if get_temp() <= 39:
        print('going to sleep for 2 minutes.')
        deepsleep(120000)
    else:
        print('going to sleep for 20 minutes.')
        deepsleep(1200000)
        
