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

leds = Leds()

def main():
    print('Waiting for button press, then we journal! (Ctrl-C for exit).')
    with Board() as board:
        while True:
            leds.pattern = Pattern.breathe(500)
            leds.update(Leds.rgb_pattern(Color.YELLOW))
            board.button.wait_for_press()
            # board.button.wait_for_release()
            print('>>> launching journal')
            board.led.state = Led.OFF
            subprocess.run(['python3', 'text_to_speech.py'])
            break


if __name__ == '__main__':
    main()
