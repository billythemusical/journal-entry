#!/usr/bin/env python3

import time
import sys
import text_to_speech

def check_the_clock(unit="hour"):
    the_time = time.localtime()
    # print("check_the_clock() the_time =", the_time.tm_min)
    if unit== "year":
        return the_time.tm_year
    elif unit== "month":
        return the_time.tm_month
    elif unit== "day":
        return the_time.tm_mday
    elif unit== "hour":
        return the_time.tm_hour
    elif unit== "min":
        return the_time.tm_min
    elif unit== "sec":
        return the_time.tm_sec
    else:
        return None

def time_to_journal(num):
    the_time = check_the_clock("min")
    if the_time == num:
        journal_time = True
        # print("it's journal time")
        return journal_time
    else:
        journal_time = False
        # print("it's not journal time")
        return journal_time

def main():

    unit = None
    num = None
    args = sys.argv[1:]
    if len(args) == 2:
        unit = sys.argv[1]
        num = int(sys.argv[2])
        # print("unit = %s, num = %d" % unit, num)
    elif len(args) == 1:
        num = int(sys.argv[1])
        # print("num =", num)

    while time_to_journal(num):
        the_time = check_the_clock("min")
        # print("the_time =", the_time)
        if the_time == num:
            print("we will journal now")
            text_to_speech()
            # return True
        else:
            # return False
            break
    exit(0)

if __name__ == '__main__':
    main()
