import time
import board
import busio
import digitalio
from adafruit_espatcontrol import adafruit_espatcontrol
from adafruit_espatcontrol import adafruit_espatcontrol_wifimanager
import adafruit_espatcontrol.adafruit_espatcontrol_socket as socket
import adafruit_requests as requests

#Button Pin
button = digitalio.DigitalInOut(board.D12)
button.direction = digitalio.Direction.INPUT
#LED Pin
led = digitalio.DigitalInOut(board.D9)
led.direction = digitalio.Direction.OUTPUT

#Webhook URL
URL = "xxx"

# Get wifi details and more from a secrets.py file. Must contain 'ssid' and 'password' at a minimum
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

uart = busio.UART(board.TX, board.RX, baudrate=115200, timeout=0.1)
resetpin = digitalio.DigitalInOut(board.D5)
rtspin = digitalio.DigitalInOut(board.D6)

esp = adafruit_espatcontrol.ESP_ATcontrol(
    uart, 115200, reset_pin=resetpin, rts_pin=rtspin, debug=False
)
esp.hard_reset()

requests.set_socket(socket, esp)

#Connect to Wifi. Will print out SSID if successful
first_pass = True
while True:
    try:
        if first_pass:
            print("Scanning for AP's")
            print("Checking connection...")
            print("Connecting...")
            esp.connect(secrets)
            print("Connected to AT software version ", esp.version)
            print("IP address ", esp.local_ip)
            first_pass = False
            break
    except (ValueError, RuntimeError, adafruit_espatcontrol.OKError) as e:
        print("Failed to get data, retrying\n", e)
        print("Resetting ESP module")
        esp.hard_reset()
        continue

#Button not pressed = LED off. Button pressed = LED on and Slack message sent
while True:
    if button.value:
        print('The button has been pressed')
        led.value = True
        try:
            r = requests.get(URL)
        except (ValueError, RuntimeError, adafruit_espatcontrol.OKError) as e:
            print("Failed to get data, retrying\n", e)
            continue
        time.sleep(0.05)
    else:
        led.value = False
