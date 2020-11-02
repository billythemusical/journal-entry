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
import os.path
from os import path
import datetime

board = Board()
leds = Leds()

def check_for_entry_today():
    date = datetime.date.today()
    date_format = "%d-%d-%d" % (date.year, date.month, date.day)
    print("the date is %s" % date_format[:4])

    path = "/home/pi/work-dir/journal-entry/entries"
    entries = os.listdir(path)
    for entry in entries:
        if date_format in entry:
            print("journaled today already 👌🏼" + entry)
            exit()

def journal():
    # turn the LED off
    board.led.state = Led.OFF
    print('>>> launching journal 📓')
    # launch the subprocess
    # subprocess.run(['python3', 'text_to_speech.py'])
    subprocess.run(['python3', '/home/pi/work-dir/journal-entry/text_to_speech.py'])
    exit(0)

def main():
    # if no entry has been made that day...
    check_for_entry_today();

    print("not journaled today 👇🏼")

    # callback to run when button is released
    board.button.when_pressed = journal

    print('waiting for press 👇🏽')

    leds.pattern = Pattern.breathe(2000)
    leds.update(Leds.rgb_pattern(Color.YELLOW))
    # board.button.wait_for_press(60*15) # 15 minutes
    board.button.wait_for_press(15) # 15 seconds
    # if no press...
    print('no press, exiting 👋🏽...')
    board.led.state = Led.OFF


if __name__ == '__main__':
    main()
