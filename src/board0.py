import time
import rfdevice
import config
import machine
import protocol

sender = rfdevice.RFDevice(tx_pin=0)
sender.enable_tx()

stage=0

while True:
    time.sleep(1)
    sender.tx_code(protocol.CODE_STAGE[stage], tx_pulselength=protocol.PULSE_LENGTH, tx_proto=protocol.PROTOCOL)
    stage= (stage + 1) % len(protocol.CODE_STAGE)
