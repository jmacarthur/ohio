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

# Display:

# If no tea is being brewed here, then just display 'tea?' or 'ohio' or some placeholder.
# Once a button is pressed, tea starts brewing for three minutes. During this phase:
# Scroll "(tea name) ready in MM:SS". Repeat the scroll every ten seconds.
# If 'cancel' is pressed, display "Cancel" for two seconds, then go back to 'no tea' mode.
# When the tea is ready, alternate "(tea name)  MMMm".
# When tea has been ready for two hours, go back to 'no tea' mode.


class State():
    def __init__(self):
        self.current_tea_index = None
        self.time_brewing_started = None
        self.message = None
        self.brewing = False
        self.message_timeout = 0
        self.scroll_position = 0

def main(stdscr):
    # Clear screen
    s = State()
    seq = 0
    x = None
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
               s.current_tea_index = v-ord('0')
               tea = lookup[s.current_tea_index]
               s.message = "{} ready in 0300".format(tea)
               s.message_timeout = 100
            if v == ord('9'):
                # Cancel
                s.message = "CANC"
                s.current_tea_index = None
                s.message_timeout = 100
            x = v

        # Update curses display
        stdscr.addstr(0,0,"Last keypress: {}".format(x))
        stdscr.addstr(1,0,"Scrolling message: >{}<".format(s.message))
        stdscr.addstr(3,0,"Message timeout: {}".format(s.message_timeout))

        # Update four-letter display
        if s.message_timeout <= 0:
            flp.clear()
            if s.message:
                flp.print_str(s.message[s.scroll_position:])
                if seq % 5 == 0 and s.scroll_position < len(s.message)-4:
                    s.scroll_position += 1
        else:
            s.message_timeout -= 1
        seq += 1
        time.sleep(0.1)
        

wrapper(main)
