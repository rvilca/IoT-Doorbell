from gpiozero import LED, Button
import time import sleep

led = LED(17)
button = Button (2)

import slack

import logging
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack import WebClient
from slack.errors import SlackApiError

# WebClient insantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
webtoken = "xxx"
client = WebClient(token=webtoken)

logger = logging.getLogger(__name__)

# ID of channel you want to post message to
channel_id = "xxx"

while True:
    if button.is_pressed:
        led.on()
        try:
            # Call the conversations.list method using the WebClient
            result = client.chat_postMessage(
            channel=channel_id,
                text="Someone is at the door!"
                # You could also use a blocks[] array to send richer content
            )
            # Print result, which includes information about the message (like TS)
            print(result)
            sleep(2)
        except SlackApiError as e:
            print(f"Error: {e}")
    else:
        led.off()