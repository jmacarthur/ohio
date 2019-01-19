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
        self.scrolling_message = None
        self.fixed_message = None
        self.brewing = False
        self.message_timeout = 0
def main(stdscr):
    # Clear screen
    s = State()

    stdscr.clear()
    stdscr.nodelay(1) # set getch() non-blocking
    tea = "TEA?"
    quit = False
    flp.clear()
    flp.print_number_str('OHIO')
    flp.show()
    while not quit:
        v = stdscr.getch()
        if v != -1:
            if v >= ord('0') and v <= ord('9') and v-ord('0') in lookup:
               tea = lookup[v-ord('0')]
               s.scrolling_message = "{} ready in ".format(tea)
               s.message_timeout = 0
            if v == ord('9'):
                # Cancel
                s.fixed_message = "CANC"
                s.message_timeout = 0
            x = v

            stdscr.add_str(0,0,"Last keypress: {}".format(v))
            stdscr.add_str(1,0,"Scrolling message: >{}<".format(s.scrolling_message))
            stdscr.add_str(2,0,"Fixed message: >{}<".format(s.fixed_message))
        # Update curses display
        stdscr.add_str(3,0,"Message timeout: {}".format(s.message_timeout))

        # Update four-letter display
        if s.message_timeout <= 0:
            flp.clear()
            if s.scrolling_message:
                flp.scroll_print(s.scrolling_message + "XXXX")
                s.message_timeout = 100
            elif s.fixed_message:
                flp.print_str(s.fixed_message)
                s.message_timeout = 100
        else:
            s.message_timeout -= 1
        time.sleep(0.1)
        

wrapper(main)
