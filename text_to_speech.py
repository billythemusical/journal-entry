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
import logging
import locale
import logging
import textwrap
import os
import time
import subprocess
from datetime import datetime
from helper_functions import gen_paths, get_location, collate
from aiy.board import Board, Led
from aiy.leds import Leds, Color, Pattern
from cloudspeech_modified import CloudSpeechClient


logging_path = '/home/pi/work-dir/journal-entry/misc/logs/text_to_speech.log'
logging.basicConfig(filename=logging_path, level=logging.INFO)
begin_log = '\n\n**************************\n' + str(datetime.now());
logging.info(begin_log)

def get_hints(language_code):
    if language_code.startswith('en_'):
        return ('goodbye',
                'new line',
                'Nell',
                'Katherine',
                'Prof G',
                'VidCode',
                'ITP')
    return None

def locale_language():
    language, _ = locale.getdefaultlocale()
    return language


def record_journal_entry():
    # turn light blue as we start up
    leds = Leds()

    parser = argparse.ArgumentParser(description='Assistant service example.')
    parser.add_argument('--language', default=locale_language())
    args = parser.parse_args()

    logging.info('Initializing for language %s...', args.language)
    hints = get_hints(args.language)
    client = CloudSpeechClient()

    heading = ""
    file_path = ""
    try:
        paths = gen_paths()
        heading = paths["heading"]
        file_path = paths["file_path"]
    except:
        print(">>> 🆘 there was an error setting the path...\n>>> saving dirty entry locally.")
        logging.warning('Unable to get the location.  Using default paths.')
        date = str(datetime.now())
        heading = date + "\n\n\n"
        file_path = os.getcwd()+"/je_error_dump_%s.txt" % date

    with Board() as board:
        with open(file_path, 'w') as dump:
            dump.write(heading)
            print('>>> please tell me about your day 👂🏼')
            while True:
                leds.pattern = Pattern.breathe(2000)
                leds.update(Leds.rgb_pattern(Color.RED))
                text = client.recognize(language_code=args.language,
                                        hint_phrases=hints,
                                        punctuation=True,
                                        )
                # client must return None when it gets a pause in speech
                if text is None:
                    continue

                logging.info(' You said: "%s"' % text)
                print("+ %s" % text)
                dump.write(text + "  ")

                if 'new line' in text.lower():
                    dump.write('\n\n')
                    logging.info('\n\n')
                elif 'cancel cancel cancel' in text.lower():
                    board.led.state = Led.OFF
                    exit(0)
                elif 'goodbye' in text.lower():
                    break

    leds.pattern = Pattern.breathe(1000)
    leds.update(Leds.rgb_pattern(Color.GREEN))
    logging.info('>>> wrapping and saving journal entry 📓')
    # try:
    #     with open(file_path) as file:
    #         lines = file.readlines()
    #         print("read the lines")
    #         with open(file_path, 'w') as wrapper:
    #             size = 70
    #             for line in lines:
    #                 print("+" + line)
    #                 if len(line) > size:
    #                     collated = collate(line, size)
    #                     for short in collated:
    #                         wrapper.write(short)
    #                         wrapper.write('\n')
    #                 else:
    #                     writer.write(line)
    # except:
    #     logging.error('There was an error wrapping %s' % file_path)
    time.sleep(3)
    board.led.state = Led.OFF

if __name__ == '__main__':
    record_journal_entry()
