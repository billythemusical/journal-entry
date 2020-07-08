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
"""...adapted to be a text to speech journaling app."""
import argparse
import locale
import logging
import textwrap
import subprocess
import json
import re
import datetime

from clock_functions import check_the_clock
from aiy.board import Board, Led
from cloudspeech_modified import CloudSpeechClient

def get_location():
    city_state = ""
    try:
        data = subprocess.check_output(["curl", "ipinfo.io"])
        location = json.dumps(data.decode("utf-8"))
        city = re.search(r"city\\\"\W\s\\\"([\w]+)", location).group(1)
        state = re.search(r"region\\\"\W\s\\\"([\w]+)", location).group(1)
        city_state = city + ", " + state
        print("Near %s" % city_state)
    except:
        print("error getting location");
    return city_state

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


def main():

    location = get_location()

    # logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(level=logging.ERROR)

    parser = argparse.ArgumentParser(description='Assistant service example.')
    parser.add_argument('--language', default=locale_language())
    args = parser.parse_args()

    logging.info('Initializing for language %s...', args.language)
    hints = get_hints(args.language)
    client = CloudSpeechClient()
    journal_entry = []

    # check the time, and once it's ready, listen for sounds

    with Board() as board:
        while True:
            board.led.state = Led.OFF
            board.led.state = Led.ON
            logging.info('Please tell me about your day...')
            text = client.recognize(language_code=args.language,
                                    hint_phrases=hints,
                                    punctuation=True)
            # client must return None when it gets a pause in speech
            if text is None:
                continue

            logging.info('You said: "%s"' % text)
            text = text.lower()
            journal_entry.append(text)

            if 'goodbye' in text:
                break

    logging.info('writing to journal');

    today = datetime.date.today()
    date_file = "%d-%d-%d" % (today.year, today.month, today.day)
    date_heading = "%d-%d-%d" % (today.month, today.day, today.year)
    clock = datetime.datetime.now().time()
    now = "%d:%d:%d" % (clock.hour, clock.minute, clock.second)

    timestamp = date_file + '_' + now
    output = open('je%s.txt' % timestamp, 'w')

    heading = date_heading + '\n' + location + '\n\n'
    output.write(heading)

    wrapped_entry = textwrap.wrap('\n'.join(journal_entry), width=64);
    # print(wrapped_entry)

    for line in wrapped_entry:
        # output.write(line + '\n')
        output.write(line + '\n')

    output.close()
    exit()

if __name__ == '__main__':
    main()
