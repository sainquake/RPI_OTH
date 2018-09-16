# -*- coding: utf-8 -*-
#!/usr/bin/env python3
#import binascii
import serial
import RPi.GPIO as GPIO
import time

print("OTH")
class OpenThermHat:
	ser = serial.Serial()
	def __init__(self):
		print("init")
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
		
		self.ser = serial.Serial ("/dev/serial0") #"/dev/ttyAMA0")    #Open named port
		self.ser.baudrate = 115200                     #Set baud rate to 9600
		self.ser.timeout = 1
	def sendReceive(self,ad0,ad1,data0,data1):
		# address0 address1 data0 data1
		values = bytearray([ad0, ad1, data0, data1])
		self.ser.write(values)
		time.sleep(0.1)
		data = self.ser.read(4)
		print('data=' , ":".join("{:02x}".format(c) for c in data))
		return int.from_bytes(data, byteorder='little')
	def setTemp(self,temp):
		return self.sendReceive(10,0,0,temp)
	def getTemp(self):
		d = self.sendReceive(11,0,0,0)
		return	(d>>16)/256.0
	def getADC(self,ch):
		d = self.sendReceive(6,ch,0,0)
		return (d>>16)/256.0
	def getBoilerID(self):
		d = self.sendReceive(3,0,0,0)
		return d>>16
	def getOpenTermStatus(self,subaddress):
		d = self.sendReceive(7,subaddress,0,0)
		return d>>16
	def getMem(self,address):
		d = self.sendReceive(8,address,0,0)
		return d>>16
oth = OpenThermHat()
while True:
	oth.sendReceive(1,0,0,4)
	time.sleep(0.5)
	oth.setTemp(52)
	time.sleep(0.5)	
	print("indorTemp=\t"+str(oth.getTemp()))
	time.sleep(0.5)	
	print ("USB Voltage=\t"+str(oth.getADC(6)))
	time.sleep(0.5)
	print("BoilerID=\t"+str(oth.getBoilerID()))
	time.sleep(0.5)
	print("BoilerSwitchedOff=\t"+str(oth.getOpenTermStatus(0)))
	time.sleep(0.5)
	print("hardware id=\t"+str(oth.getMem(0)))
