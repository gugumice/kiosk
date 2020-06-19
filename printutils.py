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

def deleteJobs(conn):
    jobs_pending = conn.getJobs()
    for j in jobs_pending:
        logging.info('Deleting pending print job {}'.format(j))
        conn.cancelJob(j,purge_job=True)
    return(len(jobs_pending))

def deletePrinters(conn):
    p=conn.getDefault()
    if p is not None:
        try:
            conn.deletePrinter(p)
        except IPPError:
            logging.error('Cannot delete printer {}'.format(p))
        else:
            logging.info('Printer {} deleted'.format(p))
    else:
        logging.info('No default printer to delete')

def listPPDs(conn,filter=None):
    ppd=conn.getPPDs()
    for p in ppd:
        if filter is not None and not ppd[p]['ppd-make-and-model'].startswith(filter):
            continue
        #print(ppd[p]['ppd-make-and-model'])
        print(p,ppd[p])

def addPrinter(conn,model='HP LaserJet Series PCL 6 CUPS'):
    usb_printers=conn.getDevices(include_schemes=['usb'])
    try:
        ppd = conn.getPPDs(ppd_make_and_model=model)
        ppd_file=[f for f in ppd][0]
    except cups.IPPError:
        logging.error('PPD for <{}> not found'.format(model))
        return False
    #print(ppd)
    for p in usb_printers:
        dev_name=usb_printers[p]['device-make-and-model']
        if dev_name.startswith('HP'):
            p_queue = dev_name.replace(' ','_')
            try:
                conn.addPrinter(p_queue,ppdname=ppd_file,device=p,info=dev_name)
                conn.setPrinterShared(p_queue,False)
                conn.setDefault(p_queue)
                conn.acceptJobs(p_queue)
                conn.enablePrinter(p_queue)
            except Exception as e:
                logging.error(e)

def printReport(conn,reportPdf):
    printReport=False
    logging.debug('Printing {}'.format(reportPdf))
    p = conn.getDefault()
    try:
        deleteJobs(conn)
        printJobID=conn.printFile(p,reportPdf,'Report', {'print-color-mode': 'monochrome'})
    except Exception as e:
        logging.debug('Error printing {} {}'.format(reportPdf,e))
    else:
        logging.info('{} printed'.format(reportPdf))
        printReport=True
    return(printReport)

def testReport(conn):
    testReport=False
    f = getReport(url)
    logging.debug('File: {}'.format(f))
    if f is not None:
        printReport(conn,f)
        testReport=True
        try:
            #pass
            os.remove(f)
        except:
            pass
    else:
        logging.error('Error getting PDF: <{}>'.format(url))
    return

def setPrinter():
    conn=cups.Connection()
    deleteJobs(conn)
    deletePrinters(conn)
    #print(conn.getDevices(limit=1,include_schemes=['usb']))
    #print(getPPDfile(conn))
    addPrinter(conn)
    printReport(conn,'/usr/share/cups/data/testprint')

def checkDefaultPrinter():
    checkDefault=True
    conn=cups.Connection()
    if conn.getDefault() == None:
        logging.info('Default printer not found. Setup init.')
        conn=None
        setPrinter()
        checkDefault=False
    return(checkDefault)
def main():
    #setPrinter()
    #testReport(conn)
    checkDefaultPrinter()

if __name__=='__main__':
   logging.basicConfig(level=logging.DEBUG)
   main()
