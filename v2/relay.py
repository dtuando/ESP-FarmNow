import network, ubinascii, espnow, json

bcast = b'\xff' * 6


mac = ubinascii.hexlify(network.WLAN(network.STA_IF).config('mac'),':').decode()
print("MAC: " + mac)

sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.config(protocol=network.MODE_LR)
e = espnow.ESPNow()
e.active(True)

def irq_cb(code, data):
    if code == espnow.EVENT_RECV_MSG:
        peer, msg = data
        if msg:
            print(msg.decode('utf-8'))
            payload = msg.decode('utf-8')
            e.send(bcast, payload)
            
e.add_peer(bcast)
    
e.irq(irq_cb)
