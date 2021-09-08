import network
from machine import Pin
import time
import urequests

sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect("DESKTOP-DB7K25S 0198", "5894Tb=9")

led = Pin(13, Pin.OUT)
button = Pin(16, Pin.IN)

while True:
    if button.value():
        print('The button has been pressed')
        led(1)
        r = urequests.get('https://maker.ifttt.com/trigger/button_pressed/with/key/sVjPZHXL3nvngBqgrHR5c')
        time.sleep(2.0)
    else:
        print('Released')
        led(0)
        time.sleep(0.5)
