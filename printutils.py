#!/usr/bin/env python3
from time import sleep
import cups
import re,os
import pycurl
import logging
from time import sleep, time

url='http://10.100.50.104/csp/sarmite/ea.kiosk.pdf.cls?HASH=13621914%238444&LANG=RUS'
#url='http://10.100.50.104/csp/sarmite/ea.kiosk.pdf.cls?HASH=13621914%138444&LANG=RUS'

CURL_TIMEOUT=30

def getReport(url):
    reportFile=None
    bc='temp_rep'
    fileDest='/tmp/{}.pdf'.format(bc)
    fileSource=url
    r=None
    try:
        with open(fileDest, 'wb') as f:
            c = pycurl.Curl()
            c.setopt(pycurl.CONNECTTIMEOUT, CURL_TIMEOUT)
            c.setopt(c.URL, fileSource)
            c.setopt(c.WRITEDATA, f)
            c.perform()
            c.close()
            r=fileDest
    except Exception as e:
        logging.error(e)
    if os.path.getsize(fileDest)<20:
        r=None
    return(r)

def printReport(reportPdf):
    logging.debug('Printing {}'.format(reportPdf))
    conn=cups.Connection()
    p = conn.getDefault()
    jobs_pending = conn.getJobs()
    for j in jobs_pending:
        logging.info('Deleting pending print job {}'.format(j))
        conn.cancelJob(j,purge_job=True)
    printJobID=conn.printFile(p,reportPdf,'Report', {'print-color-mode': 'monochrome'})

def main():
    f = get_Report(url)
    logging.debug('File: {}'.format(f))
    if f is not None:
        print_Report(f)
        try:
            #pass
            os.remove(f)
        except:
            pass
    else:
        logging.error('Error getting PDF: <{}>'.format(url))
if __name__=='__main__':
   logging.basicConfig(level=logging.DEBUG)
   main()
