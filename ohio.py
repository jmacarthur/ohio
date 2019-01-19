#!/usr/bin/env python3

import curses
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

TEA_BREWING_TIME=180 # Seconds
MAX_TEA_AGE = 120*60 # Seconds

class State():
    def __init__(self):
        self.current_tea_index = None
        self.time_brewing_started = None
        self.message = None
        self.brewing = False
        self.message_timeout = 0
        self.scroll_position = 0
        self.brewed = False
    def end_of_scroll(self):
        """ True if we can scroll and have finished scrolling. """
        return (self.scroll_position > len(self.message)-4) and len(self.message)>4

    def reset_scroll(self):
        self.scroll_position = -4

    def get_scroll_pos(self):
        return 0 if self.scroll_position < 0 else self.scroll_position

def main(stdscr):
    # Clear screen
    s = State()
    seq = 0
    x = None
    stdscr.clear()
    stdscr.nodelay(1) # set getch() non-blocking
    s.message = "Tea?"
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
               s.message = "{} ready in ????".format(tea)
               s.message_timeout = 120
               s.time_brewing_started = time.localtime()
               s.brewing = True
               s.reset_scroll()
            if v == curses.KEY_BACKSPACE:
                # Cancel
                s.message = "CANC"
                s.current_tea_index = None
                s.message_timeout = 20
                s.time_brewing_started = None
                s.brewing = False
                s.reset_scroll()
            x = v

        # Update curses display for debugging
        stdscr.addstr(0,0,"Last keypress: {}".format(x))
        stdscr.addstr(1,0,"Scrolling message: >{}<".format(s.message))
        stdscr.addstr(2,0,"Scroll position: >{}<".format(s.get_scroll_pos()))
        stdscr.addstr(3,0,"Message timeout: {}".format(s.message_timeout))
        if s.time_brewing_started:
            stdscr.addstr(4,0,"Brewing started: {}:{}:{}".format(s.time_brewing_started.tm_hour, s.time_brewing_started.tm_min, s.time_brewing_started.tm_sec))
            stdscr.addstr(5,0,"Brewing started: {}s".format(time.mktime(s.time_brewing_started)))
        else:
            stdscr.addstr(4,0,"Nothign brewing")
        stdscr.addstr(6,0,"Time now : {}s".format(time.mktime(time.localtime())))

        # Update tea time, if currently brewing
        if s.time_brewing_started:
            elapsed = time.mktime(time.localtime()) - time.mktime(s.time_brewing_started)
            remaining = int(TEA_BREWING_TIME-elapsed)
            if remaining > 0:
                s.message = s.message [:-4] + "{:1d}m{:02d}".format(int(remaining/60), remaining%60)
            else:
                if s.brewing:
                    s.reset_scroll()
                s.brewing = False
                tea = lookup[s.current_tea_index]
                s.message = "{} {:3d}m".format(tea, int((elapsed - TEA_BREWING_TIME)/60))

            if elapsed > MAX_TEA_AGE:
                s.time_brewing_started = None
                s.current_tea_index = None
                s.brewing = False
                s.message = "Tea?"                
                s.reset_scroll()

        # Update four-letter display
        if s.message_timeout > 0:
            flp.clear()
            if s.message:
                flp.print_str(s.message[s.get_scroll_pos():])
                if seq % 5 == 0 and s.scroll_position < len(s.message)-4:
                    s.scroll_position += 1
            flp.show()
            s.message_timeout -= 1
        else:
            if s.current_tea_index:
                s.reset_scroll()
                s.message_timeout = 120
            else:
                flp.clear()
                s.message = "Tea?"                
                flp.print_str(s.message)
                flp.show()
        seq += 1
        time.sleep(0.1)
        
curses.wrapper(main)
