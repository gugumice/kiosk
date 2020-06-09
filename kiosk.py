
#!/usr/bin/env python3

import argparse
from printutils import getReport, printReport
from leds import ledButtons, pushButtons

import serial
import re
from time import sleep
import threading
import logging

BUTTON_PINS=(17,27,22)
LED_PINS=(13,19,26)
BUZ_PIN=12
HOST='10.100.50.104'
PORT='/dev/ttyACM0'
DEFAULT_BUTTON=0
LANGUAGES=('LAT','ENG','RUS')
BUTTON_TIMEOUT=10 #Button timeout in secs
URL='http://{}/csp/sarmite/ea.kiosk.pdf.cls?HASH={}&LANG={}'
logging.basicConfig(filename='/home/pi/kiosk.log',filemode='w',level=logging.DEBUG)
#logging.basicConfig(level=logging.DEBUG)

class barCodeReader(object):
    def __init__(self, port='/dev/ttyACM0',
                 timeout=.3):
        self.running=False
        try:
             self.fp=serial.Serial(port=port,timeout=timeout)
             self.running=True
        except Exception as e:
             logging.error('Canot open: {}\n{}'.format(port,e))
    def next(self):
        try:
            return(self.fp.readline().decode('ascii').rstrip('\r\n'))
        except serial.serialutil.SerialException:
            logging.error('Lost communications with BC')
            self._running=False
def update_leds(l,b):
    logging.debug('Active button: {}'.format(b))
    l.off()
    l.on(b,s=True)
    return(b)

def make_URL(bc,host,lang):
    req_url=None
    req_code = re.search('^#\d{7,9}#\d{4,5}',bc)
    if req_code is not None:
        req_code = req_code.group(0)
        req_code=req_code[1:].replace('#','%23')
        req_url=URL.format(host,req_code,lang)
    return(req_url)

def make_report(url):
    make_report=False
    f=getReport(url)
    if f is not None:
        printReport(f)
        make_report=True
        try:
            os.remove(f)
        except:
            logging.error('Error deleting {}.'.format(f))
    return(make_report)

def main(port=None,host=None):
    #Watchdog
    wdog=True
    try:
        wd=open('/dev/watchdog','w')
        logging.info('Watchdog enabled')
    except:
        wdog=False
        logging.error('Watchdog disabled')
    active_button=DEFAULT_BUTTON
    running=False
    leds=ledButtons(LED_PINS,BUZ_PIN)
    bttn=pushButtons(BUTTON_PINS,timeout=BUTTON_TIMEOUT)
    rep_file=None
    if port is None:
        port=PORT
    if host is None:
        host=HOST
    bcr=barCodeReader(port)

    if bcr.running:
        leds.blink(n=1,t=.2,s=True)
        sleep(.5)
        leds.on(DEFAULT_BUTTON)
        running=True
    else:
        leds.blink(n=5,s=True)
    try:
        while running:
            if bttn.pressed() is not None:
                b=bttn.pressed()
                active_button=update_leds(leds,b)
            if bttn.timed_out():
                if active_button != DEFAULT_BUTTON:
                    active_button=update_leds(leds,DEFAULT_BUTTON)
            rep_code=bcr.next()
            if len(rep_code) > 0:
                u=make_URL(rep_code,host,LANGUAGES[active_button])
                logging.debug('URL {}, BC {}'.format(u,rep_code))
                if u is not None:
                    t = threading.Thread(target=make_report, args=(u,))
                    t.start()
                    bttn.reset()
                    logging.info('Report thread started')
                    while t.is_alive():
                        leds.wave()
                leds.off()
                leds.on(active_button)
            else:
                #Watchdog
                if wdog:
                    print(1,file = wd, flush = True)
    except KeyboardInterrupt:
        if wdog:
            print('V',file = wd, flush = True)
        running=False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Print report')
    parser.add_argument('-port', metavar='port', type=str, help='Port for barcode reader')
    parser.add_argument('-host', metavar='host', type=str, help='5M host')
    args = parser.parse_args()
    main(port=args.port,host=args.host)
