#!/usr/bin/env python3

# We put this script in our Crontab to run each day at a conveniet time.
# Once the user sees the light blinking, they can click the button
# to begin the text_to_speech script.  When the light blinks red,
# the user can begin speaking.

# One feature to add would be for the app to check if we have journaled that day,
# and blink every 15 minutes at the top of the hour until we do get an entry.
# Or to have it listen for sounds from a person in the room, and then trigger the light
# and wait for a button press.


from aiy.board import Board, Led
from aiy.leds import Leds, Color, Pattern
import subprocess
import time

board = Board()
leds = Leds()

def journal():
    # turn the LED off
    board.led.state = Led.OFF
    print('>>> launching journal 📓')
    # launch the subprocess
    subprocess.run(['python3', 'text_to_speech.py'])
    exit(0)

def main():
    # callback to run when button is released
    board.button.when_pressed = journal

    print('waiting for press 👇🏽')

    leds.pattern = Pattern.breathe(2000)
    leds.update(Leds.rgb_pattern(Color.YELLOW))
    # button waits for 60 seconds times 15 minutes
    board.button.wait_for_press(60*15)
    # if no press...
    print('no press, exiting 👋🏽...')
    board.led.state = Led.OFF


if __name__ == '__main__':
    main()
