#!/usr/bin/env python
import sys
import time
import serial
import struct
import logging

logging.basicConfig(filename='/home/pi/Xbee/ReceiveLogs/receiveAT.log',level=logging.DEBUG,format='%(asctime)s %(message)s')

ser = serial.Serial(
	port='/dev/ttyACM0',
	baudrate = 115200,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1
)

def serialReader():
    b = ser.read()
    if b:
        bs = struct.unpack("<B",b)
        return int(bs[0])
    else:
        return -1

#while ser.in_waiting:
while True:
        #print("Reading info")
        if serialReader() == 255 and serialReader() == 255:
            length = serialReader()
            data = [0]*length
            for x in xrange(length):
                data[x] = serialReader()
            if data[0] == 0: # 0 means an UPDATE_INFO package
                dev = [data[6],data[11]]
                logging.info(data)
                print dev
            

#while count<11:
#	ser.write(values)
#	time.sleep(1)
#	count+=1
