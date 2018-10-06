# -*- coding: utf-8 -*-
#!/usr/bin/env python3
#import binascii
import serial
import RPi.GPIO as GPIO
import time

print("OTH")
class OTData:
	#otStatus
	otTimeout = 0
	otIndex = 0
	otBusy = 0
	otComplete = 0
	otFrameSendedAndStartWaitingACK = 0
	otReadingResponse = 0
	otSpecialRequest = 0
	otSpecialRequestComplete = 0
	#boilerStatus
	boilerFault = 0
	boilerCHMode = 0
	boilerDHWMode = 0
	boilerFlameStatus = 0
	boilerCoolingStatus = 0
	boilerCH2Mode = 0
	boilerDiagnostic = 0
	#boilerConfig
	boilerMemberID = 0
	boilerDHWPresent = 0
	boilerControlType = 0
	boilerCoolingConfig = 0
	boilerDHWConfig = 0
	boilerPumpControlFunction = 0
	boilerCH2Present = 0
	#errorConfig
	errorOEM = 0
	errorServiceRequered = 0
	errorLockoutReset = 0
	errorLowWaterPress = 0
	errorGasFlameFault = 0
	errorAirPressureFault = 0
	errorWaterOverTemperature = 0
	def __init__(self,otStatus,boilerStatus,boilerConfig,errorFlags):
		otTimeout = otStatus&1
		otIndex = otStatus>>8&0xFF
		otBusy = otStatus>>1&1
		otComplete = otStatus>>2&1
		otFrameSendedAndStartWaitingACK = otStatus>>3&1
		otReadingResponse = otStatus>>4&1
		otSpecialRequest = otStatus>>5&1
		otSpecialRequestComplete = otStatus>>6&1
		#boilerStatus
		boilerFault = boilerStatus&1
		boilerCHMode = (boilerStatus>>1)&1
		boilerDHWMode = (boilerStatus>>2)&1
		boilerFlameStatus = (boilerStatus>>3)&1
		boilerCoolingStatus = (boilerStatus>>4)&1
		boilerCH2Mode = (boilerStatus>>5)&1
		boilerDiagnostic = (boilerStatus>>6)&1
		#boilerConfig
		boilerMemberID = boilerConfig&0xFF
		boilerDHWPresent = (boilerConfig>>8)&1
		boilerControlType = (boilerConfig>>9)&1
		boilerCoolingConfig = (boilerConfig>>10)&1
		boilerDHWConfig = (boilerConfig>>11)&1
		boilerPumpControlFunction = (boilerConfig>>12)&1
		boilerCH2Present = (boilerConfig>>13)&1
		#errorConfig
		errorOEM = errorFlags&0xFF
		errorServiceRequered = (errorFlags>>8)&1
		errorLockoutReset = (errorFlags>>9)&1
		errorLowWaterPress = (errorFlags>>10)&1
		errorGasFlameFault = (errorFlags>>11)&1
		errorAirPressureFault = (errorFlags>>12)&1
		errorWaterOverTemperature = (errorFlags>>13)&1
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
	otData = OTData(0,0,0,0)
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
		#self.reset(False)
		#time.sleep(1)
		#self.reset(True)
		#time.sleep(1)
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
	def resetMCU(self):
		self.reset(False)
		time.sleep(1)
		self.reset(True)
		time.sleep(1)
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
		d = self.getBoilerReg((1<<7) +1,temp*256)/256.0
		if self.addressMatchError>0:
			self.addressMatchError=0
			return None
		return d
	def setTempCH2(self,temp):
		d = self.getBoilerReg((1<<7) +8,temp*256)/256.0
		if self.addressMatchError>0:
			self.addressMatchError=0
			return None
		return d
	def setRoomTargetTemp(self,temp):
		d = self.getBoilerReg((1<<7) +16,temp*256)/256.0
		if self.addressMatchError>0:
			self.addressMatchError=0
			return None
		return d
	def setRoomTargetTempCH2(self,temp):
		d = self.getBoilerReg((1<<7) +23,temp*256)/256.0
		if self.addressMatchError>0:
			self.addressMatchError=0
			return None
		return d
	def setRoomTemp(self,temp):
		d = self.getBoilerReg((1<<7) +24,temp*256)/256.0
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
	def getOTStatus(self):
		otStatus = self.getOpenTermStatus(6)
		boilerStatus = self.getBoilerReg(0)
		boilerConfig = oth.getBoilerReg(3)
		errorFlags = oth.getBoilerReg(5)
		otData = OTData(otStatus,boilerStatus,boilerConfig,errorFlags)
		return	otData
	def getADC(self,ch):
		d = self.sendReceive(self.RPi_ADC_UART_ADDRESS,ch,0,0)
		if self.addressMatchError>0:
			self.addressMatchError=0
			return None
		return ((d>>16)&0xFFFF)/256.0
	def getBoilerReg(self,address,da=0):
		d = self.sendReceive(self.RPi_OT_UART_ADDRESS,address,da&0xFF,(da>>8)&0xFF)
		if self.addressMatchError>0:
			self.addressMatchError=0
			return None
		d = (d>>16)&0xFFFF
		return d
	def getBoilerHeader(self,address):
		d = self.sendReceive(32,address,0,0)
		if self.addressMatchError>0:
			self.addressMatchError=0
			return None
		d = (d>>16)&0xFFFF
		return d
	def getBoilerID(self):
		d = self.sendReceive(self.RPi_OT_UART_ADDRESS,3,0,0)
		if self.addressMatchError>0:
			self.addressMatchError=0
			return None
		d = (d>>16)&0xFFFF
		#print("P:"+str(d>>15)+"\tMSG-TYPE:"+str(d>>12))
		return d
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