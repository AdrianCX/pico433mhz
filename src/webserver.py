import network
import socket
import time
import re
import rfdevice
import config
import machine

def wait_wlan(wlan):
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)

    if wlan.status() != 3:
        print("Failed setting up wifi, will restart in 30 seconds")
        time.sleep(30)
        machine.reset()

def setup_ap():
    wlan = network.WLAN(network.AP_IF)
    wlan.config(essid=config.WIFI_SSID, password=config.WIFI_PASSWORD) 
    wlan.active(True)
    wait_wlan(wlan)
    
    print('set up access point:', config.WIFI_SSID, 'with ip = ', wlan.ifconfig()[0])
    return wlan

def connect_wlan():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    wlan.disconnect()
    
    wlan.active(True)
    wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)

    wait_wlan(wlan)
    
    print('connected to wifi:', config.WIFI_SSID, 'with ip = ', wlan.ifconfig()[0])
    return wlan

wlan = connect_wlan() if not config.WIFI_AP_MODE else setup_ap()

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(socket.getaddrinfo('0.0.0.0', config.PORT)[0][-1])
s.listen(10)

sender = rfdevice.RFDevice()
sender.enable_tx()
receiver = rfdevice.RFDevice()

while True:
    try:
        cl, addr = s.accept()

        try:
            print('client connected from', addr)
            request = cl.recv(1024)
            m = re.search("GET /(receive|send)[/]?([0-9]*)?[/]?([0-9]*)[/]?([0-9]*)? HTTP", str(request))
        
            if m is None:
                raise Exception("Request did not match regex 'GET /(receive|send)[/]?([0-9]*)?[/]?([0-9]*)[/]?([0-9]*)? HTTP'\r\nUser either did not request HTTP, or sent to a unknown URL\r\nFull Request: " + str(request) + "\r\n")
                
            if m.group(1) == "receive":
                receiver.enable_rx()
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
                receiver.disable_rx()
            if m.group(1) == "send":
                sender.tx_code(int(m.group(2)), int(m.group(3)), int(m.group(4)))
                cl.sendall('HTTP/1.0 200 OK\r\n\r\n')
                
            cl.close()
        except Exception as e:
            cl.sendall('HTTP/1.0 500 Internal Server Error\r\nContent-type: text/html\r\n\r\n')
            cl.sendall(str(e))
            cl.close()
    except Exception as e:
        print('failed accepting socket, continue')
