import time
import rfdevice
import machine
import protocol

receiver = rfdevice.RFDevice(rx_pin=1)
receiver.enable_rx()

timestamp = None

# Idea - send periodic signal every 1 second so everyone is synchronized even if they missed receiving it.
while True:
    time.sleep(0.050)
    if receiver.rx_code_timestamp != timestamp:
        timestamp = receiver.rx_code_timestamp
        if timestamp != None:
            print('{ "code": "' + str(receiver.rx_code) + '", "pulselength": "' + str(receiver.rx_pulselength) + '", "protocol": "' + str(receiver.rx_proto) + '" }')

            if receiver.rx_pulselength == protocol.PULSE_LENGTH and receiver.rx_proto == protocol.PROTOCOL:
                code = receiver.rx_code

                for i in range(0, len(protocol.CODE_STAGE)):
                    if protocol.CODE_STAGE[i] == int(code):
                        print("Stage:" + str(i+1))
                    
