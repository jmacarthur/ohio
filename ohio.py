#!/usr/bin/env python3

from curses import wrapper
import fourletterphat as flp
import time

lookup = {
 0: 'EARL',
 1: 'CYLN',
 2: 'ASAM',
 3: 'DARJ',
 4: 'RUSC',
 5: 'LAPS' }

class State():
    def __init__(self):
        self.current_tea = ''
        self.time_brewing_started = None

def main(stdscr):
    # Clear screen
    s = State()

    stdscr.clear()
    stdscr.nodelay(1) # set getch() non-blocking
    tea = "TEA?"
    seq = 0
    quit = False
    flp.clear()
    flp.print_number_str('OHIO')
    flp.show()
    while not quit:
        v = stdscr.getch()
        if v != -1:
            if v >= ord('0') and v <= ord('9') and v-ord('0') in lookup:
               tea = lookup[v-ord('0')]
               flp.clear()
               flp.scroll_print("Brewing {}".format(tea))
               flp.show()
            x = v
        seq += 1
        time.sleep(0.1)

wrapper(main)
