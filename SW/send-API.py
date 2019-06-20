#!/usr/bin/env python
import sys
import time
import serial
import logging

logging.basicConfig(filename='/home/pi/Xbee/SendLogs/sentAPI.log',level=logging.DEBUG,format='%(asctime)s %(message)s')

ser = serial.Serial(
	port='/dev/ttyACM0',
	baudrate = 115200,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1
)

if len(sys.argv)<2:
	param = bytearray([0x8C,0x5A])
	logging.warning('API Package non-definde values')
else:
	param = sys.argv[1]
	
val1 = param[0]+param[1]
val2 = param[3]+param[4]
var1 = int(val1,16)
var2 = int(val2,16)

checksum_rha = (~(6+2+var1+var2+125) & 0xFF)
checksum_xbee = (~(16+1+5*255+254+6+2+var1+var2+125+checksum_rha) & 0xFF)

if var1>124 and var1<167 and var2>59 and var2<111:
        values = bytearray([0x7E, 0x00, 0x16, 0x10, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFE, 0x00, 0x00, 0xFF, 0xFF, 0x06, 0x02, 0x7D, var1, var2, checksum_rha, checksum_xbee])

        #print(hex(values[x]))
                
        ser.write(values)
        logging.info('API Package sent')
        
else:
        logging.warning('API Package out of range')
