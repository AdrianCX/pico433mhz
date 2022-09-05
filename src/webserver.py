import network
import socket
import time
import re
import rfdevice
import config
import machine

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)

max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

if wlan.status() != 3:
    print("Failed connecting to wifi, will restart in 30 seconds")
    time.sleep(30)
    machine.reset()
else:
    status = wlan.ifconfig()
    print('connected with ip = ' + status[0] )

addr = socket.getaddrinfo('0.0.0.0', config.PORT)[0][-1]

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)

print('listening on ', status[0], ':', config.PORT)

sender = rfdevice.RFDevice()
sender.enable_tx()
    
receiver = rfdevice.RFDevice()
receiver.enable_rx()

while True:
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        m = re.search("GET /(receive|send)[/]?([0-9]*)?[/]?([0-9]*)[/]?([0-9]*)? HTTP", str(request))
        
        if m.group(1) == "receive":
            cl.sendall('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n[')
            timestamp = None
            start = time.ticks_ms()
            while time.ticks_ms() - start < 15000:
                if receiver.rx_code_timestamp != timestamp:
                    timestamp = receiver.rx_code_timestamp
                    if timestamp != None:
                        cl.sendall('{ "code": "' + str(receiver.rx_code) + '", "pulselength": "' + str(receiver.rx_pulselength) + '", "protocol": "' + str(receiver.rx_proto) + '" }')
                    else:
                        cl.sendall(',\n{ "code": "' + str(receiver.rx_code) + '", "pulselength": "' + str(receiver.rx_pulselength) + '", "protocol": "' + str(receiver.rx_proto) + '" }')        
                time.sleep(0.5)
            cl.send(']')
        if m.group(1) == "send":
            sender.tx_code(int(m.group(2)), int(m.group(3)), int(m.group(4)))
            cl.sendall('HTTP/1.0 200 OK\r\n\r\n')
                
        cl.close()
    except OSError as e:
        print(e)
        cl.close()
        print('connection closed')