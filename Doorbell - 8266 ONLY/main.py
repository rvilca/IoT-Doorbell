import network
from machine import Pin
import time
import urequests

sta = network.WLAN(network.STA_IF)
sta.active(True)
ssid = "xxxxx"
password = "xxxxx"
sta.connect(ssid, password)

led = Pin(13, Pin.OUT)
button = Pin(16, Pin.IN)

URL = 'xxxx'

while True:
    if button.value():
        print('The button has been pressed')
        led(1)
        r = urequests.get(URL)
        time.sleep(2.0)
    else:
        print('Released')
        led(0)
        time.sleep(0.5)
