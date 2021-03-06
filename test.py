
#!/usr/bin/env python3

from leds import ledButtons, pushButtons
from time import sleep
import logging

BUTTON_PINS=(17,27,22)
LED_PINS=(13,19,26)
BUZ_PIN=12
DEFAULT_BUTTON=0
BUTTON_TIMEOUT=5

#logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(filename='/home/pi/test.log',filemode='w',level=logging.DEBUG)

def update_leds(l,b):
    logging.debug('Active button: {}'.format(b))
    l.off()
    l.on(b,s=True)
    return(b)

def main():
    logging.debug('Test LED PINs {}, Button pins {}, buzzer {}'.format(LED_PINS,BUTTON_PINS,BUZ_PIN))
    leds=ledButtons(LED_PINS,BUZ_PIN)
    bttn=pushButtons(BUTTON_PINS,timeout=BUTTON_TIMEOUT)
    leds.blink(n=3,t=1,s=True)
    sleep(.5)
    leds.on(DEFAULT_BUTTON)
    running=True
    try:
        while running:
            if bttn.pressed() is not None:
                b=bttn.pressed()
                logging.info('Button {} pressed'.format(b))
                active_button=update_leds(leds,b)
            if bttn.timed_out():
                if active_button != DEFAULT_BUTTON:
                    logging.info('Button {} timeout. Reset to default {}'.format(active_button,DEFAULT_BUTTON))
                    active_button=update_leds(leds,DEFAULT_BUTTON)

    except KeyboardInterrupt:
        running=False

if __name__ == '__main__':
     main()
