# -*- coding: utf-8 -*-
#!/usr/bin/env python3
#import binascii
import serial
import RPi.GPIO as GPIO
import time

print("OTH")
class OpenThermHat:
	RPI_BUFFER_SIZE=5
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
	crcError = 0
	addressMatchError = 0
	def __init__(self):
		print("init")
		# Use "logical" pin numbers
		GPIO.setmode(GPIO.BCM)
		# Disable "This channel is already in use" warnings
		GPIO.setwarnings(False)
		# Setup MCU POWER UP
		#GPIO.setup(self.POWER, GPIO.OUT)
		#GPIO.output(self.POWER, True)
		self.powerOn(True)
		time.sleep(1)
		self.reset(False)
		time.sleep(1)
		self.reset(True)
		time.sleep(1)
#		GPIO.setup(18, GPIO.OUT)
#		GPIO.output(18, True)
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
	def powerOn(self,b):
		GPIO.setup(self.POWER, GPIO.OUT)
		GPIO.output(self.POWER, b)
	def reset(self,b):
		GPIO.setup(18, GPIO.OUT)
		GPIO.output(18, b)
	def sendReceive(self,ad0,ad1,data0,data1):
		# address0 address1 data0 data1
		values = bytearray([ad0, ad1, data0, data1,(ad0+ad1+data0+data1)&0xFF])
		self.ser.write(values)
		time.sleep(0.1)
		data = self.ser.read(self.RPI_BUFFER_SIZE)
		if len(data) == 0:
			self.timeouts+=1
		if self.timeouts>5:
			self.timeouts=0
			#GPIO.output(self.POWER, False)
			#time.sleep(2)
			#GPIO.output(self.POWER, True)
		#	print("RESET")
		#print('data=' , ":".join("{:02x}".format(c) for c in data))
		if int.from_bytes(data, byteorder='little')&0xFF==255:
		#	print("CRC ERROR")
			self.ser.flushInput()
			self.ser.flushOutput()
			crcError = 1
		#	return None
		if int.from_bytes(data, byteorder='little')&0xFF!=ad0:
		#	print("SEND ADDR!=RECEIVED ADDR")
			self.ser.flushInput()
			self.ser.flushOutput()
			addressMatchError =1
		#	return None
		return int.from_bytes(data, byteorder='little')
	def ledControl(self,pin,state):
		GPIO.output(pin, state)
	def setTemp(self,temp):
		d = self.sendReceive(self.RPi_SET_TEMP_UART_ADDRESS,0,0,temp)
		if self.addressMatchError>0:
			self.addressMatchError=0
			return None
		return d
	def getTemp(self):
		d = self.sendReceive(self.RPi_GET_HW_TEMP_UART_ADDRESS,0,0,0)
		if self.addressMatchError>0:
			self.addressMatchError=0
			return None
		return	((d>>16)&0xFFFF)/256.0
	def getADC(self,ch):
		d = self.sendReceive(self.RPi_ADC_UART_ADDRESS,ch,0,0)
		if self.addressMatchError>0:
			self.addressMatchError=0
			return None
		return ((d>>16)&0xFFFF)/256.0
	def getBoilerID(self):
		d = self.sendReceive(self.RPi_OT_UART_ADDRESS,0,0,0)
		if self.addressMatchError>0:
			self.addressMatchError=0
			return None
		return (d>>16)&0xFFFF
	def getOpenTermStatus(self,subaddress):
		d = self.sendReceive(self.RPi_OT_STATUS_UART_ADDRESS,subaddress,0,0)
		if self.addressMatchError>0:
			self.addressMatchError=0
			return None
		return (d>>16)&0xFFFF
	def getMem(self,address):
		d = self.sendReceive(self.RPI_MEM_UART_ADDRESS,address,0,0)
		if self.addressMatchError>0:
			self.addressMatchError=0
			return None
		return (d>>16)&0xFFFF
	def getGSM(self,address,d1=0,d2=0):
		d = self.sendReceive(self.RPi_SIM800L_UART_ADDRESS,address,d1,d2)
		if self.addressMatchError>0:
			return None
		return (d>>16)&0xFFFF
	def getOperator(self):
		#d = self.sendReceive(self.RPi_SIM800L_UART_ADDRESS,7,0,0)
		#return d>>16
		self.ser.flushInput()
		values = bytearray([self.RPi_SIM800L_UART_ADDRESS,7,0,0,(self.RPi_SIM800L_UART_ADDRESS+7+0+0)&0xFF])
		self.ser.write(values)
		time.sleep(0.3)
		data = self.ser.readline()
		self.ser.flushInput()
		#print('data=' , ":".join("{:02x}".format(c) for c in data))
		self.addressMatchError=0
		return data
	def getSMS(self,num):
		self.ser.flushInput()
		values = bytearray([self.RPi_SIM800L_UART_ADDRESS,24,num,0,(self.RPi_SIM800L_UART_ADDRESS+24+num+0)&0xFF])
		self.ser.write(values)
		time.sleep(0.3)
		data = self.ser.readlines()
		self.ser.flushInput()
		self.addressMatchError=0
		#print('data=' , ":".join("{:02x}".format(c) for c in data))
		return data

