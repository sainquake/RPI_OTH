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

#time.sleep(1)
#GPIO.setup([10,11,8], GPIO.IN)
#GPIO.output([10,11,8], False)
#time.sleep(2)
#GPIO.setup([10,11,8], GPIO.OUT)
#GPIO.output([10,11,8], True)
#time.sleep(2)
#GPIO.cleanup([10,11,8])
#time.sleep(2)

#spi = spidev.SpiDev()
#spi.open(0, 0)
#spi.max_speed_hz = 1560000
#spi.max_speed_hz = 976000

# Split an integer input into a two byte array to send via SPI
#def write_pot(input):
#        hsb = input >> 16 & 0xFF
#        msb = input >> 8 & 0xFF
#        lsb = input & 0xFF
#        spi.xfer([hsb, msb, lsb])

i=0
# SEND SPI
while True:
        ser.write("Hel") 
	time.sleep(0.1)
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
