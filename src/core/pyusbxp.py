#-------------------------------------------------------------------------------
# Name:        PyUsbXpresse  pyusbxp.py
# Purpose:     Python wrapper for UsbXpresse API
#
# Author:      nkom@rocketmail.com
#
# Ref:         http://www.silabs.com/Support%20Documents/TechnicalDocs/an169.pdf
#
# Created:     06/04/2013
# Copyright:   (c) nkom 2013
# Licence:     LGPL
#
#
# Installation: Simply put this module and SiUSBxp.dll in anywherer python can access.
#               SiUSBxp.dll can be found in
#                    C:\Program Files\Polimaster\PM PRD PoliIdentify Software
#               or   C:\Program Files (x86)\Polimaster\PM PRD PoliIdentify Software
#
#               You can get it from Silicon lab's USBXpress developement kit
#                   http://www.silabs.com/products/mcu/Pages/USBXpress.aspx
#
#
# ver. 0.22 2013-04-08
#       Some functions added. Few functions are still missing.
#
# ver. 0.1  2013-04-06
#       Initial release
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import time
import sys
from os.path import join, dirname
from ctypes import *
from ctypes.wintypes import *

r_code = {
0x00:"SI_SUCCESS",
0xFF:"SI_DEVICE_NOT_FOUND",
0x01:"SI_INVALID_HANDLE",
0x02:"SI_READ_ERROR",
0x03:"SI_RX_QUEUE_NOT_READY",
0x04:"SI_WRITE_ERROR",
0x05:"SI_RESET_ERROR",
0x06:"SI_INVALID_PARAMETER",
0x07:"SI_INVALID_REQUEST_LENGTH",
0x08:"SI_DEVICE_IO_FAILED",
0x09:"SI_INVALID_BAUDRATE",
0x0a:"SI_FUNCTION_NOT_SUPPORTED",
0x0b:"SI_GLOBAL_DATA_ERROR",
0x0c:"SI_SYSTEM_ERROR_CODE",
0x0d:"SI_READ_TIMED_OUT",
0x0e:"SI_WRITE_TIMED_OUT",
0x0f:"SI_IO_PENDING",

0x1f:"waitRX_time_out"

}

def sleep(ms): time.sleep(float(ms)/ 1000)

class UsbxpError( Exception ): pass
ex = UsbxpError

class Usbxp(object):
    def __init__(self, dbg = 0):
        if getattr(sys, 'frozen', False):
            self.si = windll.SiUSBxp
        else:
            name = {
                False: '../../win32/x86/SiUSBXp.dll',
                True: '../../win32/x64/SiUSBXp.dll'}[sys.maxsize > 2**32]
            self.si = windll.LoadLibrary(join(dirname(__file__),name))
        self.h = HANDLE()
        self.dbg = dbg
        self.o = 0
        self.nd = self._number()

    def __del__(self, r = 0):
        # Destructer and error habdling
        if r and self.dbg:
            print "UsbxpError: %s" % r_code[r]
        if self.o:
            self.close()
        if r:
            raise ex(r_code[r])

    def _number(self):
        #SI_STATUS SI_GetNumDevices (LPDWORD NumDevices)
        nd = DWORD()
        r = self.si.SI_GetNumDevices(byref(nd))
        if r: self.__del__(r)
        return nd.value

    def list(self):
        self.ndev = self._number()
        #SI_GetProductString (DWORD DeviceNum, LPVOID DeviceString, DWORD Options)
        dsp = c_char_p('\0' * 256)
        #define SI_RETURN_SERIAL_NUMBER 0x00
        #define SI_RETURN_DESCRIPTION 0x01
        #define SI_RETURN_LINK_NAME 0x02
        #define SI_RETURN_VID 0x03
        #define SI_RETURN_PID 0x04
        self.l = []
        for dn in range(self.ndev):
            ll = []
            for i in range(5):
                r = self.si.SI_GetProductString(DWORD(dn), dsp, DWORD(i))
                if r: self.__del__(r)
                ll.append(dsp.value)
            self.l.append(ll)
        return self.l

    def open(self, dn =0):
        self.dn = dn
        if self.nd == 1: self.dn = 0
        if self.o:
            self.__del__()
            msleep(500)
        r = self.si.SI_Open(DWORD(self.dn), byref(self.h))
        if r: self.__del__(r)
        self.o = 1
        if self.dbg: print "USBXpress opened"
        return self.h

    def close(self):
        # SI_Close (HANDLE Handle)
        r = self.si.SI_Close(self.h)
        if self.dbg: print "USBXpress closed"
        if r: raise ex(r_code[r])
        self.o = 0

    def read(self, nb):
        # SI_STATUS SI_Read (HANDLE Handle, LPVOID Buffer, DWORD NumBytesToRead,
        # DWORD *NumBytesReturned, OVERLAPPED* o = NULL)
        buf = (c_ubyte * 4096)()
#        o = c_char_p('\0' * 4096)
        nr = DWORD()
#        r = self.si.SI_Read(self.h, byref(buf), DWORD(nb), byref(nr), 0)
        r = self.si.SI_Read(self.h, buf, DWORD(nb), byref(nr), None)
        if r: self.__del__(r)
        s = bytearray(buf[:nr.value])
        return s


    def write(self, s = ""):
        s = str(s)
        # SI_STATUS SI_Write (HANDLE Handle, LPVOID Buffer, DWORD NumBytesToWrite,
        # DWORD *NumBytesWritten, OVERLAPPED* o = NULL)
        buf = c_char_p(s)
        nb = DWORD()
        r = self.si.SI_Write(self.h, buf, DWORD(len(s)), byref(nb), 0)
        if self.dbg: print "Usbxp.write(): '%s' %d %s" % (s, nb.value, r_code[r])
        if r: self.__del__(r)
        return nb.value

    def writeln(self, s = ""):
        return self.write(s + "\r\n")

    def waitSO(self):
        #WaitForSingleObject()
        pass

    def settimeout(self, rt = 100, wt = 100):
        # SI_SetTimeouts (DWORD ReadTimeout, DWORD WriteTimeout)
        r = self.si.SI_SetTimeouts(DWORD(rt), DWORD(wt))
        if r: self.__del__(r)
        return self.gettimeout()

    def gettimeout(self):
        # SI_STATUS SI_GetTimeouts (LPDWORD ReadTimeout, LPDWORD WriteTimeout)
        rt = DWORD()
        wt = DWORD()
        r = self.si.SI_GetTimeouts(byref(rt), byref(wt))
        if r: self.__del__(r)
        return (rt.value,wt.value)

    def checkRX(self):
        # SI_CheckRXQueue (HANDLE Handle, LPDWORD NumBytesInQueue, LPDWORD QueueStatus)
        nb = DWORD()
        qs = DWORD()
        r = self.si.SI_CheckRXQueue(self.h, byref(nb), byref(qs))
        if r: self.__del__(r)
        return  (nb.value, qs.value)

    def waitRX(self, tout = 15000):
        iv = 100
        x = int(tout / iv)
        for i in range(x):
            r = self.checkRX()
            if r[1] == 2: return r
            sleep(iv)
        if self.dbg: print "waitRX:", x, i
        self.__del__(0x1f)

    def flush(self):
        r = self.si.SI_FlushBuffers(self.h, BYTE(1), BYTE(1))
        if r: self.__del__(r)

    def status(self):
        b = BYTE(0)
        r = self.si.SI_GetModemStatus(self.h, byref(b))
        if r: self.__del__(r)
        return b.value

    def setbr(self, br = 9600):
        r = self.si.SI_SetBaudRate(self.h, DWORD(br))
        if r: self.__del__(r)

    def setlc(self, lc):
        r = self.si.SI_SetLineControl(self.h, WORD(lc))
        if r: self.__del__(r)

    def setbreak(self, bs = 0):
        # bs = 1:  Set break.    bs = 0 reset break
        r = self.si.SI_SetBreak(self.h, WORD(bs))
        if r: self.__del__(r)

    def getpn(self):
        b = BYTE(0)
        r = self.si.SI_GetPartNumber(self.h, byref(b))
        if r: self.__del__(r)
        return b.value


def main():
    # List USBXpress devices
    u = Usbxp()
    print u._number()
    l = u.list()
    print l

if __name__ == '__main__':
    main()
