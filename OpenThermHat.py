# -*- coding: utf-8 -*-
#!/usr/bin/env python3
#import binascii
import serial
import RPi.GPIO as GPIO
import time

print("OTH")
class OpenThermHat:
	RPI_BUFFER_SIZE=4
	RPi_ECHO_UART_ADDRESS=1
	RPi_BLINK_UART_ADDRESS=2
	RPi_OT_UART_ADDRESS=				3
	RPi_DS18B20_UART_ADDRESS=		4
	RPi_SIM800L_UART_ADDRESS=		5
	RPi_ADC_UART_ADDRESS=			6
	RPi_OT_STATUS_UART_ADDRESS=		7
	RPI_MEM_UART_ADDRESS=			8

	RPi_SET_TEMP_UART_ADDRESS=       10
	RPi_GET_HW_TEMP_UART_ADDRESS=    11
	
	POWER=17
	RED=4
	GREEN=27
	BLUE=6
	ser = serial.Serial()
	timeouts=0
	def __init__(self):
		print("init")
		# Use "logical" pin numbers
		GPIO.setmode(GPIO.BCM)
		# Disable "This channel is already in use" warnings
		GPIO.setwarnings(False)
		# Setup MCU POWER UP
		GPIO.setup(self.POWER, GPIO.OUT)
		GPIO.output(self.POWER, True)
		#LEDS
		GPIO.setup(self.RED, GPIO.OUT)
		GPIO.output(self.RED, True)
		
		GPIO.setup(self.GREEN, GPIO.OUT)
		GPIO.output(self.GREEN, True)
		
		GPIO.setup(self.BLUE, GPIO.OUT)
		GPIO.output(self.BLUE, True)
		
		self.ser = serial.Serial ("/dev/serial0") #"/dev/ttyAMA0")    #Open named port
		self.ser.baudrate = 115200                     #Set baud rate to 9600
		self.ser.timeout = 2
	def sendReceive(self,ad0,ad1,data0,data1):
		# address0 address1 data0 data1
		values = bytearray([ad0, ad1, data0, data1])
		self.ser.write(values)
		time.sleep(0.1)
		data = self.ser.read(self.RPI_BUFFER_SIZE)
		if len(data) == 0:
			self.timeouts+=1
		if self.timeouts>5:
			self.timeouts=0
			GPIO.output(self.POWER, False)
			time.sleep(2)
			GPIO.output(self.POWER, True)
			print("RESET")
		print('data=' , ":".join("{:02x}".format(c) for c in data))
		return int.from_bytes(data, byteorder='little')
	def ledControl(self,pin,state):
		GPIO.output(pin, state)
	def setTemp(self,temp):
		return self.sendReceive(self.RPi_SET_TEMP_UART_ADDRESS,0,0,temp)
	def getTemp(self):
		d = self.sendReceive(self.RPi_GET_HW_TEMP_UART_ADDRESS,0,0,0)
		return	(d>>16)/256.0
	def getADC(self,ch):
		d = self.sendReceive(self.RPi_ADC_UART_ADDRESS,ch,0,0)
		return (d>>16)/256.0
	def getBoilerID(self):
		d = self.sendReceive(self.RPi_OT_UART_ADDRESS,0,0,0)
		return d>>16
	def getOpenTermStatus(self,subaddress):
		d = self.sendReceive(self.RPi_OT_STATUS_UART_ADDRESS,subaddress,0,0)
		return d>>16
	def getMem(self,address):
		d = self.sendReceive(self.RPI_MEM_UART_ADDRESS,address,0,0)
		return d>>16
	def getGSM(self,address):
		d = self.sendReceive(self.RPi_SIM800L_UART_ADDRESS,address,0,0)
		return d>>16
	def getOperator(self):
		#d = self.sendReceive(self.RPi_SIM800L_UART_ADDRESS,7,0,0)
		#return d>>16
		self.ser.flushOutput()
		values = bytearray([self.RPi_SIM800L_UART_ADDRESS,7,0,0])
		self.ser.write(values)
		time.sleep(0.3)
		data = self.ser.readline()
		self.ser.flushOutput()
		#print('data=' , ":".join("{:02x}".format(c) for c in data))
		return data
