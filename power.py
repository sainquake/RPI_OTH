

#!/usr/bin/env python

import serial
import RPi.GPIO as GPIO
import time

# Use "logical" pin numbers
GPIO.setmode(GPIO.BCM)
# Disable "This channel is already in use" warnings
GPIO.setwarnings(False)

# Setup MCU POWER UP
GPIO.setup(17, GPIO.OUT)
GPIO.output(17, True)
#LEDS
GPIO.setup(4, GPIO.OUT)
GPIO.output(4, True)

GPIO.setup(27, GPIO.OUT)
GPIO.output(27, True)

GPIO.setup(6, GPIO.OUT)
GPIO.output(6, True)

ser = serial.Serial ("/dev/ttyAMA0")    #Open named port 
ser.baudrate = 115200                     #Set baud rate to 9600
ser.timeout = 1
#data = ser.read(10)                     #Read ten characters from serial port to data#
#ser.write(data)                         #Send back the received data
#ser.close() 


i=0
while True:
    #ser.write("Hel")
	#start of request to hardware
	# address0 address1 data0 data1 
	values = bytearray([11, 0, 0, 0])
	ser.write(values)
	time.sleep(0.1)
	data = ser.read(4)
	print 'data=' , ":".join("{:02x}".format(ord(c)) for c in data)
	#temp = 0
	#temp = data[2]<<8 + data[3];
	#print temp
	#end of request for HardWare
	time.sleep(0.5)
	GPIO.output(4,False)
	GPIO.output(27,False)
	GPIO.output(6,False)
	if i==3:
		i=0
	if i==0:
		GPIO.output(4,True)
	if i==1:
                GPIO.output(27,True)
	if i==2:
                GPIO.output(6,True)
	i += 1
