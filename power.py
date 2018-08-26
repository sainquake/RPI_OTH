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
#data = ser.read(10)                     #Read ten characters from serial port to data#
#ser.write(data)                         #Send back the received data
#ser.close() 


i=0
while True:
    #ser.write("Hel")
	# address0 address1 data0 data1 
	values = bytearray([1, 0, 3, 4])
	ser.write(values)
	data = ser.read(4)
	print 'data=' , data
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
