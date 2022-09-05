Simple raspberry pi pico 433mhz receiver/transmitter controlled via http

![Alt text](/pictures/endproduct.jpg "")


# 1. How to use when all set up

## 1.1. Sniffing traffic

a. Start receiver via a HTTP call. Press remote button you want to sniff a few times once you get 200 OK.
   After 15 seconds it will return all sniffed keys.

```
curl -v "http://192.168.100.196:80/receive"
*   Trying 192.168.100.196:80...
* Connected to 192.168.100.196 (192.168.100.196) port 80 (#0)
> GET /receive HTTP/1.1
> Host: 192.168.100.196
> User-Agent: curl/7.81.0
> Accept: */*
> 
* Mark bundle as not supporting multiuse
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Content-type: text/html
< 
* Closing connection 0
[{ "code": "14012112", "pulselength": "350", "protocol": "1" }]
```

## 1.2. Sending codes

API: http://[ip-address]/send/[code]/[protocol]/[pulselength]

example:
```
curl -v "http://192.168.100.196:80/send/14012112/1/350"
```

And light should turn on and off.


# 2. How to set up software once built

Set up micropython on pico (use the firmware for 'Raspberry Pi Pico W (with urequests and upip preinstalled)')
URL https://www.raspberrypi.com/documentation/microcontrollers/micropython.html

Update 'src/config.py' with your SSID and password.
Copy all files from src to pico. (you can use thonny for this)

Run webserver.py code with Thonny. (or rename to main.py and let pico run on each reboot)
It will print the IP address it obtains once it starts up. You can also obtain the IP address from your router and ideally assign a DNS and static IP.


# 3. How to make this

### 3.1. Parts used:

a. Raspberry pi pico
- https://www.kiwi-electronics.com/nl/raspberry-pi-pico-w-10938?search=raspberry%20pi%20pico

b. DollaTek 5pcs 433MHz receiver and wireless
- https://www.amazon.nl/-/en/dp/B07DJYK29J/ref=sr_1_5?crid=1VFFGXXVM8YAG&keywords=433+mhz&sprefix=433mhz%2Caps%2C72&sr=8-5


c. Cables (1x40) - 4.29 (only need ~4 depending on skill)
- AZDelivery Jumper Wire Cable 40 pieces per 20cm F2F Female to Female compatible with Arduino and Raspberry Pi Including E-Book!
- https://www.amazon.nl/-/en/dp/B07KYHBVR7/ref=sr_1_15?crid=2GCQ7CNPDNBI4&keywords=jumper+wire+raspberry&sprefix=jumper+wire+raspberry%2Caps%2C71&sr=8-15

d. Either
- micro-usb cable - 1.25E - https://www.kiwi-electronics.com/nl/microusb-kabel-usb-a-naar-micro-b-15cm-3240?search=microusb%20
- OR charger - Raspberry Pi PSU 5.1V 2.5A MicroUSB - EU-plug - https://www.kiwi-electronics.com/nl/raspberry-pi-psu-5-1v-2-5a-microusb-eu-plug-10809?search=microusb%20

e. Extra fun pieces:
- An Ace black heart
- double sided tape
- some M2 screws (x4 or x6 length), nuts and washers to fix raspberry pi (to avoid double sided tape on it)
- - https://www.amazon.nl/-/en/dp/B08FWTVXDG/ref=sr_1_6?crid=1V9X0MRZYXJKF&keywords=m2*6+moeren&sprefix=m2+6+nuts%2Caps%2C65&sr=8-6
- electric cable to use as antenna (17.2cm or longer straight wire for transmitting things)


### 3.2. Notes on steps:

It's a lot easier to do with breadboard.

We only have one 3.3V port, so we'll need to connect that to the TX/RX pair, I just cut a cable and connected the copper.
There are multiple ground ports but I used the same trick as for 3.3V

Did not solder (I should), it still works fine with copper twisted to the pin.
Pins for data are GPIO 27/22.

The antenna is a simple power copper wire, should be 17.2cm and straight. It goes into the antenna port on 433 TX. (can chip at cable with cutter until it fits if it's too large).

Without antenna, there's not enough power to transmit more then a few cm. (same for receiver)
The 433mhz rx/tx pair work fine with 3.3V.

Tools needed:
![Alt text](/pictures/whatsneeded.jpg "")

This replaces old style remotes for led lights:
![Alt text](/pictures/replacement.jpg "")

### 3.3. Antenna

For antenna I used regular copper wire that is normally used for wiring lights inside house.
Any copper wire will work if it's held straight (including the jumper cables above, I tried, they work fine)
I used solid core since it will stay straight without anything else holding it.

Measure to 17.5 or higher: (since we're gonna cut up a bit)
![Alt text](/pictures/antenna_1.jpg "")

Chip at copper until it can fit the antenna port
![Alt text](/pictures/antenna_2.jpg "")

Push the cabble through back of the card inside the port. (Then twist the other end so it doesn't come loose)
![Alt text](/pictures/antenna_3.jpg "")

Use some tape or glue or both on the other side to have antenna stuck on card
![Alt text](/pictures/antenna_4.jpg "")
