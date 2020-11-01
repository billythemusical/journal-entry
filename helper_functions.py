#!/usr/bin/env python3

import sys
import subprocess
import os
import datetime
import json
import re

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
    if city_state:
        return city_state
    else:
        return "Location N/A"

def gen_paths():
    # entry_path = os.path.abspath(os.getcwd()) + "/entries/"
    entry_path = "/home/pi/work-dir/journal-entry/entries/"
    location = get_location();
    today = datetime.date.today()
    date_file = "%d-%d-%d" % (today.year, today.month, today.day)
    date_heading = "%d-%d-%d" % (today.month, today.day, today.year)
    heading = date_heading + '\nnear ' + location + '\n\n'

    clock = datetime.datetime.now().time()
    hour_min_sec = "%d-%d-%d" % (clock.hour, clock.minute, clock.second)

    timestamp = date_file + '_' + hour_min_sec
    file_path = entry_path + 'je%s.txt' % timestamp
    paths = { 'entry_path':entry_path, 'file_path':file_path, 'heading':heading }
    # print(path_works)
    return paths

def collate(text, size):
    new_text = []
    split_char = 1
    while split_char > 0:
        comma = str.find(text, ',', size)
        space = str.find(text, ' ', size)
        dot = str.find(text, '.', size)

        split_char = min(max(comma, dot), max(comma, space), max(dot, space))

        if text[:split_char]:
            new_text.append(text[:split_char])
        text = text[split_char+1:].replace('\n', "")

        # if split_char == size:
        #     break
    return new_text

# gen = gen_file_path()
# print(gen['heading'])
# exit(0)
