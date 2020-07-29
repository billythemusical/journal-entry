#!/usr/bin/env python3

# A simple script to turn off the AIY led if a process leaves it on.
# Note that this will not kill the process associated with the Led,
# but just overwrites the current Led state.

from aiy.board import Board, Led
board = Board()
board.led.state = Led.OFF
print("We turned the Led off 🤙🏼")
