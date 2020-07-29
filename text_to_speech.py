#!/usr/bin/env python3
#
# Adapted from Google's AIY Cloudspeech Demo
#
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""A demo of the Google CloudSpeech recognizer..."""
"""...adapted to be a text-to-speech journaling app."""
import argparse
import locale
import logging
import textwrap
import os
import time
import subprocess
import datetime
from helper_functions import gen_paths, get_location
from aiy.board import Board, Led
from aiy.leds import Leds, Color, Pattern
from cloudspeech_modified import CloudSpeechClient

def get_hints(language_code):
    if language_code.startswith('en_'):
        return ('turn on the light',
                'turn off the light',
                'blink the light',
                'goodbye')
    return None

def locale_language():
    language, _ = locale.getdefaultlocale()
    return language


def record_journal_entry():
    # turn light blue as we start up
    leds = Leds()
    logging.basicConfig(level=logging.INFO)
    # logging.basicConfig(level=logging.DEBUG)
    # logging.basicConfig(level=logging.ERROR)

    parser = argparse.ArgumentParser(description='Assistant service example.')
    parser.add_argument('--language', default=locale_language())
    args = parser.parse_args()

    logging.info('Initializing for language %s...', args.language)
    hints = get_hints(args.language)
    client = CloudSpeechClient()
    journal_entry = ""

    # check the time, and once it's ready, listen for sounds
    # subprocess.Popen(["python3", "led_breathe.py", "-d", "10", "-br", "-c", "RED"]);
    with Board() as board:
        while True:
            leds.pattern = Pattern.breathe(500)
            leds.update(Leds.rgb_pattern(Color.RED))
            logging.info('Please tell me about your day...')
            text = client.recognize(language_code=args.language,
                                    hint_phrases=hints,
                                    punctuation=True,
                                    )
            # client must return None when it gets a pause in speech
            if text is None:
                continue

            logging.info('You said: "%s"' % text)
            # text = text.lower()
            journal_entry += text + " "

            if 'new line' in text.lower():
                journal_entry.replace('new line', '\n\n    ')
            elif 'cancel cancel cancel' in text.lower():
                board.led.state = Led.OFF
                exit(0)
            elif 'goodbye' in text.lower():
                break

    leds.pattern = Pattern.breathe(500)
    leds.update(Leds.rgb_pattern(Color.GREEN))
    logging.info('writing to journal')

    heading = ""
    file_path = ""

    try:
        paths = gen_paths()
        heading = paths["heading"]
        file_path = paths["file_path"]
    except:
        print("There was an error setting the path. Saving dirty entry locally.")
        date = str(datetime.datetime.now())
        with open("je_error_dump_%s.txt" % date, 'w') as dump:
            data = date + "\n\n\n" + journal_entry
            dump.write(data)
        board.led.state = Led.OFF
        exit(0)
    output = open(file_path, 'w')
    # output.write(heading)
    wrapped_entry = textwrap.fill(heading + journal_entry, width=70);
    # wrapped_string = "\n".join(wrapped_entry)
    output.write(wrapped_entry)
    output.close()
    board.led.state = Led.OFF




if __name__ == '__main__':
    record_journal_entry()
