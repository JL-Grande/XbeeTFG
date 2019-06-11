#!/usr/bin/env python
import sys
import time
import serial

ser = serial.Serial(
	port='/dev/ttyACM0',
	baudrate = 9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1
)

if len(sys.argv)<2:
	param = bytearray([0x7C,0x7C])
else:
	param = sys.argv[1]
	val1 = param[0]+param[1]
	val2 = param[3]+param[4]

	checksum_rha = (~(6+2+int(val1,16)+int(val2,16)+125) & 0xFF)
	checksum_xbee = (~(16+1+5*255+254+6+2+int(val1,16)+int(val2,16)+125+checksum_rha) & 0xFF)

values = bytearray([0x7E, 0x00, 0x16, 0x10, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFE, 0x00, 0x00, 0xFF, 0xFF, 0x06, 0x02, 0x7D, int(val1,16), int(val2,16), checksum_rha, checksum_xbee])
count = 0

for x in range(0,26):
	print(hex(values[x]))

while count<11:
	ser.write(values)
	time.sleep(1)
	count+=1
