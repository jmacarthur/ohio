# ohio

Ohio is software for a Raspberry Pi to provide a remote physical interface to [https://github.com/jmacarthur/utah-teabot](utah-teabot).

Status: Prerelease, unlikely to work as is.

It requires a Raspberry Pi with wifi, ideally a Pi Zero W, and a phttps://shop.pimoroni.com/products/four-letter-phat](Four letter PHAT) to use as display. It also requires a USB numeric keyboard. A normal keyboard can be used, but it's bulky.

# Installation

* Configure the Raspberry Pi with ssh and wifi.
* Install the Four letter PHAT software as per Pimoroni's instructions.
* Use `sudo raspi-config` and select `Boot Options` -> `Desktop / CLI` -> `Console Autologin`
* Add the following lines to the end of `.bashrc` for the pi user:

    # If we're the first console, start the console app
    if [ $(tty) == /dev/tty1 ]; then
       /home/pi/ohio/ohio.py
    fi

