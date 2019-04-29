# -*- coding: utf-8 -*-
#!/usr/bin/env python3
#import binascii
import serial
import RPi.GPIO as GPIO
import time
import binascii
import re

import board
import neopixel

import math 

print("OTH")

class WS281X:
	def __init__(self):
		self.pixels = neopixel.NeoPixel(board.D12, 12, brightness=0.2, auto_write=False,pixel_order=neopixel.GRB)
	def wheel(self,pos):
		# Input a value 0 to 255 to get a color value.
		# The colours are a transition r - g - b - back to r.
		if pos < 0 or pos > 255:
			r = g = b = 0
		elif pos < 85:
			r = int(pos * 3)
			g = int(255 - pos*3)
			b = 0
		elif pos < 170:
			pos -= 85
			r = int(255 - pos*3)
			g = 0
			b = int(pos*3)
		else:
			pos -= 170
			r = 0
			g = int(pos*3)
			b = int(255 - pos*3)
		return (r, g, b)
	def rainbow_cycle(self,wait):
		for j in range(255):
			for i in range(12):
				pixel_index = (i * 256 // 12) + j
				self.pixels[i] = self.wheel(pixel_index & 255)
			self.pixels.show()
			time.sleep(wait)
	def fill(self,col):
		self.pixels.fill(col)
		self.pixels.show()
	def set(self,num,col):
		self.pixels[num] = col
		self.pixels.show()
	def percent(self,p):
		#for j in range(255):
		for i in range(12):
			if i<p*11:
				self.pixels[i] = (255,255,255)
			else:
				self.pixels[i] = (0,0,0)
			if i==math.floor(p*11):
				n = math.floor((i-math.floor(p*11))*255)
				self.pixels[i] = (n,n,n)
		self.pixels.show()	
class GSM:
	def __init__(self):
		print("init /dev/ttyUSB0")
		self.ser = serial.Serial("/dev/ttyUSB0")
		self.ser.baudrate = 9600
		self.ser.timeout = 2
		self.OK = False
		#
		self.SIMInserted = False
		self.unicNumber = 0
		self.batteryCharge = 0
		self.batteryVoltage = 0
		self.signalQuality = 0
		self.operator = ""
		#
		self.balance = 0
		self.balanceRequered = False
		#
		self.smsRequered = False
		self.smsNumber = "+79063280423"
		self.smsMessage = "test from OTH"
		self.smsSent = False
		#
		self.lastSMS = ""
	def sendReceive(self, data,delay=0):
		self.OK = False
		self.ser.write(data.encode())
		if delay>0:
			time.sleep(delay)
		result = self.ser.readlines()
		self.OK = self.checkOK(result)
		return result
	def getSMSCount(self):
		req = self.sendReceive("AT+CPMS?\r\n")
		if not self.OK:
			print(req)
			return False
		return int(str(req[1],'ascii').split(',')[1])
	def readSMS(self,num):
		req = self.sendReceive("AT+CMGR="+str(num)+"\r\n")
		if not self.OK:
			print(req)
			return False
		return str(req[2],'ascii')
	def readLastSMS(self):
		lastSMSNumber = str(self.getSMSCount())
		req = self.readSMS(lastSMSNumber)#sendReceive("AT+CMGR="+lastSMSNumber+"\r\n")
		if not self.OK:
			print(req)
			return False
		try:
			req = binascii.unhexlify(req).decode('utf-16-be')
		except Exception:
			req = req
		#print(req)
		self.lastSMS = str(req)
		return str(req)
	def deleteAllSMS(self):
		return self.sendReceive("AT+CMGDA=\"DEL ALL\"\r\n")
	def getUnicNumber(self):
		req = self.sendReceive("AT+GSN\r\n")
		self.unicNumber = str(req[1],'ascii')
		return str(req[1],'ascii')
	def getBatteryCharge(self):
		req = self.sendReceive("AT+CBC\r\n")
		self.batteryCharge = int(str(req[1],'ascii').split(',')[1])
		return int(str(req[1],'ascii').split(',')[1])
	def getBatteryVoltage(self):
		req = self.sendReceive("AT+CBC\r\n")
		self.batteryVoltage = float(str(req[1],'ascii').split(',')[2])/1000
		return float(str(req[1],'ascii').split(',')[2])/1000
	def getBalance(self):
		if not self.balanceRequered:
			self.balanceRequered=True
			req = self.sendReceive("AT+CUSD=1,\"#105#\"\r\n",20)
			sms = str(req[3],'ascii').split('"')
			try:
				req = binascii.unhexlify(sms[1]).decode('utf-16-be')
			except Exception:
				req = sms[1]
			self.balance = float(re.findall("\d+\.\d+", req)[0])
			self.balanceRequered=False
			return float(re.findall("\d+\.\d+", req)[0])
		else: 
			return self.balance
	def getOperator(self):
		req = self.sendReceive("AT+CSPN?\r\n")
		if not self.OK:
			print(req)
			return str(False)
		op = str(req[1],'ascii').split('"')[1]
		self.operator = str(op)
		return str(op)
	def sendSMS(self,phone_number = " ",message = " "):
		if not self.smsRequered:
			self.smsRequered = True
			if phone_number!=" ":
				self.smsNumber = phone_number
			if message!=" ":
				self.smsMessage = message
			req = self.sendReceive("AT+CMGF=1\r\n")
			if self.OK:
				req = self.sendReceive("AT+CMGS=\""+self.smsNumber+"\"\r\n")
				if self.checkOK(req,">"):
					time.sleep(1)
					self.sendReceive(self.smsMessage)
					time.sleep(0.1)
					self.sendReceive("\x1a")
					self.sendReceive("AT\r\n")
					self.smsSent = True
					return self.OK
				else:
					return False
			else:
				self.smsSent = false
				return False
			self.smsRequered = False
		else:
			return False
	def initHTTP(self,apn="ainternet.tele2.ru",user="tele2",pwd="tele2"):
		print(self.sendReceive("AT+SAPBR=0,1\r\n",5))
		#print(gsm.sendReceive("AT+CSTT=\"ainternet.tele2.ru\",\"tele2\",\"tele2\"\r\n"))
		print(self.sendReceive("AT+SAPBR=3,1,\"CONTYPE\",\"GPRS\"\r\n"))
		print(self.sendReceive("AT+SAPBR=3,1,\"APN\",\""+apn+"\"\r\n"))
		print(self.sendReceive("AT+SAPBR=3,1,\"USER\",\""+user+"\"\r\n"))
		print(self.sendReceive("AT+SAPBR=3,1,\"PWD\",\""+pwd+"\"\r\n"))
		print(self.sendReceive("AT+SAPBR=1,1\r\n",5))
		print(self.sendReceive("AT+SAPBR=2,1\r\n"))
		print(self.sendReceive("AT+HTTPINIT\r\n",3))
		print(self.sendReceive("AT+HTTPPARA=\"CID\",1\r\n"))
	def HTTP(self,url):
		self.sendReceive("AT+HTTPPARA=\"URL\",\""+url+"\"\r\n")
		self.sendReceive('AT+HTTPACTION=0\r\n',3)
		return self.sendReceive('AT+HTTPREAD\r\n',10)
	def disableHTTP(self):
		gsm.sendReceive('AT+HTTPTERM\r\n')
		return self.OK
	def getSignalQuality(self):
		req = self.sendReceive("AT+CSQ\r\n")
		signal = int(str(req[1],"ascii").split(" ")[1].split(",")[0])
		self.signalQuality = signal*100/31
		return signal
	def checkOK(self,req,s="OK"):
		OK=False
		for member in req:
			if str(member,'ascii').find(s)>=0:
				OK=True
		return OK
	def isEnabled(self):
		req = self.sendReceive("AT\r\n")
		return self.OK
	def getPhoneFunctionality(self):
		req = self.sendReceive("AT+CFUN?\r\n")
		num = int(  re.findall("\d+", str(req[1],"ascii"))[0] )
		return num
	def isSIMInserted(self,b=True):
		req = self.sendReceive("AT+CMEE=2\r\n")
		#print(req)
		req = self.sendReceive("AT+CPIN?\r\n")
		self.SIMInserted = False if self.checkOK(req,"SIM not inserted") else True
		if b:
			return False if self.checkOK(req,"SIM not inserted") else True
		else:
			return "SIM not inserted" if self.checkOK(req,"SIM not inserted") else req
		#signal = int(str(req[1],"ascii").split(" ")[1].split(",")[0])
		#return req
	def softwareReset(self):
		req = self.sendReceive("AT+CFUN=1,1\r\n",15)
		return req	
	def getCOPS(self):
		req = self.sendReceive("AT+COPS?\r\n")
		#signal = int(str(req[1],"ascii").split(" ")[1].split(",")[0])
		return req
	def getPhoneActivityStatus(self,numerical=False):
		req = self.sendReceive("AT+CPAS\r\n")
		num = int(  re.findall("\d+", str(req[1],"ascii"))[0] )
		if numerical:
			return num
		else:
			return "Ready" if num is 0 else "Unknown" if num is 2 else "Ringing" if num is 3 else "Call in progress" if num is 4 else None
	def close(self):
		self.ser.close()
		
class OTResp:
	def __init__(self,type_=0,id_=-1,value_=0,timeout_=0,complete_=0,whileBreak_=0):
		self.type = type_
		self.id = id_
		self.value = value_
		self.timeout = timeout_
		self.complete = complete_
		self.whileBreak = whileBreak_
		self.error = 0
class OTData:
	def __init__(self,otStatus,boilerStatus,boilerConfig,errorFlags):
		self.otTimeout = otStatus&1
		self.otIndex = otStatus>>8&0xFF
		self.otBusy = otStatus>>1&1
		self.otComplete = otStatus>>2&1
		self.otFrameSendedAndStartWaitingACK = otStatus>>3&1
		self.otReadingResponse = otStatus>>4&1
		self.otSpecialRequest = otStatus>>5&1
		self.otSpecialRequestComplete = otStatus>>6&1
		self.otNoResponse = otStatus>>7&1
		#boilerStatus
		self.boilerFault = boilerStatus&1
		self.boilerCHMode = (boilerStatus>>1)&1
		self.boilerDHWMode = (boilerStatus>>2)&1
		self.boilerFlameStatus = (boilerStatus>>3)&1
		self.boilerCoolingStatus = (boilerStatus>>4)&1
		self.boilerCH2Mode = (boilerStatus>>5)&1
		self.boilerDiagnostic = (boilerStatus>>6)&1
		#boilerConfig
		self.boilerMemberID = boilerConfig&0xFF
		self.boilerDHWPresent = (boilerConfig>>8)&1
		self.boilerControlType = (boilerConfig>>9)&1
		self.boilerCoolingConfig = (boilerConfig>>10)&1
		self.boilerDHWConfig = (boilerConfig>>11)&1
		self.boilerPumpControlFunction = (boilerConfig>>12)&1
		self.boilerCH2Present = (boilerConfig>>13)&1
		#errorConfig
		self.errorOEM = errorFlags&0xFF
		self.errorServiceRequered = (errorFlags>>8)&1
		self.errorLockoutReset = (errorFlags>>9)&1
		self.errorLowWaterPress = (errorFlags>>10)&1
		self.errorGasFlameFault = (errorFlags>>11)&1
		self.errorAirPressureFault = (errorFlags>>12)&1
		self.errorWaterOverTemperature = (errorFlags>>13)&1
	def printClass(self):
		attrs = self.__dict__
		print (', ' '\n'.join("%s: %s" % item for item in attrs.items()) )
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
	
	RPi_OT_HEADER_UART_ADDRESS= 32
	RPi_OT_REQUEST_ADDRESS= 33
	RPi_OT_COMPLETE_ADDRESS= 34
	RPi_OT_RESPONSE_ADDRESS= 35
	RPi_OT_ACTIVATE_ADDRESS=36

	RPi_SET_TEMP_UART_ADDRESS=       10
	RPi_GET_HW_TEMP_UART_ADDRESS=    11
	
	POWER=17
	RED=4
	GREEN=27
	BLUE=6
	nRST=18
	ser = serial.Serial()
	timeouts=0
	crcError = 0
	addressMatchError = 0
	
	otStatus = 0
	boilerStatus = 0
	boilerConfig = 0
	errorFlags = 0
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
		#nRST as pull up input
		GPIO.setup(self.nRST, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.add_event_detect(self.nRST, GPIO.BOTH)  # add rising edge detection on a channel
		GPIO.add_event_callback(self.nRST, self.resetEvent)
		#time.sleep(1)
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
		self.otData = OTData(0,0,0,0)
	def resetEvent(self,channel):
		if GPIO.input(self.nRST):
			print('nRST was HIGH (WORKING STATE)')
			self.ledControl(self.RED,False)
		else:
			print('nRST was LOW (RESET STATE)')
			self.ledControl(self.RED,True)
	def powerOn(self,b):
		GPIO.setup(self.POWER, GPIO.OUT)
		GPIO.output(self.POWER, b)
	def reset(self,b):
		if b:
			GPIO.setup(self.nRST, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		else:
			GPIO.setup(self.nRST, GPIO.OUT)
			GPIO.output(self.nRST, b)
	def isEnabled(self):
		echo = self.sendReceive(self.RPi_ECHO_UART_ADDRESS,0,4,5)
		return (echo>>16)&0xFFFF == 0x0504
	def resetMCU(self):
		self.reset(False)
		time.sleep(1)
		self.reset(True)
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
	def OT(self, type_, id_,  value_):
		self.ledControl(self.GREEN,not GPIO.input(self.GREEN))
		self.OTRequest(type_, id_,  value_)
		self.otStatus = self.getOpenTermStatus(6)
		self.otData = OTData(self.otStatus,self.boilerStatus,self.boilerConfig,self.errorFlags)
		while not self.otData.otSpecialRequestComplete and not self.otData.otTimeout:
			self.otStatus = self.getOpenTermStatus(6)
			self.otData = OTData(self.otStatus,self.boilerStatus,self.boilerConfig,self.errorFlags)
			time.sleep(0.3)
		#if not self.otData.otSpecialRequestComplete:
		#	print("not otSpecialRequestComplete")
		#if self.otData.otTimeout:
		#	print("otTimeout")
		tmp = self.OTResponseHeader()
		return OTResp(tmp>>12,tmp&0xFF,self.OTResponse(),self.otData.otTimeout,self.otData.otSpecialRequestComplete,0)
	def OTRequest(self, type_, id_,  value_):
		d = self.sendReceive(self.RPi_OT_REQUEST_ADDRESS,(type_<<7)+id_,value_&0xFF,(value_>>8)&0xFF)
		d = (d>>16)&0xFFFF
		return d
	def OTRequestComplete(self):
		d = self.sendReceive(self.RPi_OT_COMPLETE_ADDRESS,0,0,0)
		d = (d>>16)&0xFFFF
		return d
	def OTResponseHeader(self):
		d = self.sendReceive(self.RPi_OT_RESPONSE_ADDRESS,0,0,0)
		d = (d>>16)&0xFFFF
		return d
	def OTResponse(self):
		d = self.sendReceive(self.RPi_OT_RESPONSE_ADDRESS,1,0,0)
		d = (d>>16)&0xFFFF
		return d
	def OTActivate(self):
		d = self.sendReceive(self.RPi_OT_ACTIVATE_ADDRESS,0,0,0)
		d = (d>>16)&0xFFFF
		return d
	def getOpenTermStatus(self,subaddress):
		d = self.sendReceive(self.RPi_OT_STATUS_UART_ADDRESS,subaddress,0,0)
		if self.addressMatchError>0:
			self.addressMatchError=0
			return None
		return (d>>16)&0xFFFF
	def isOTEnabled(self):
		i=10
		while not self.getConfiguration():
			#print("Boiler is not enabled; check powering or opentherm connection wire")
			time.sleep(0.3)
			if i==0:
				return False
			i -= 1
		
		return True
	def getConfiguration(self):
		out = self.OT(0,3,0)
		
		if (out.type != 4) or (out.id != 3):
			return False
		else:
			print("type"+str(out.type)+ " id" +str(out.id) + " value" + str(out.value))
		return True
	def doOTUntilIDMatch(self,type_, id_,  value_):
		out = self.OT(type_,id_,value_)
		i=10
		while out.id!=id_:
			out = self.OT(type_,id_,value_)
			print( "not match "+str(10-i))
			time.sleep(0.1)
			if i==0:
				print("error 123")
				out.error = 1
				return out
			i -= 1
		return out
	def setOTStatus(self,i=0):
		#self.otStatus = self.getOpenTermStatus(6)
		#self.boilerStatus = self.getBoilerReg(0)
		#self.boilerConfig = self.getBoilerReg(3)
		#self.errorFlags = self.getBoilerReg(5)
		out = self.doOTUntilIDMatch(0,0,i<<8)
		#if out.type is 4:
		self.boilerStatus = out.value
		self.otData = OTData(self.otStatus,self.boilerStatus,self.boilerConfig,self.errorFlags)
		print(out.error)
		return	out		
	def setTemp(self,temp):
		out = self.doOTUntilIDMatch(1,1,temp*256)
		return out.value/256.0
	def setDHWTemp(self,temp):
		out = self.doOTUntilIDMatch(1,56,temp*256)
		if out.id!=56:
			return False
		return out.value/256.0
	#sensors
	def getRelativeModulationLevel(self):
		out = self.doOTUntilIDMatch(0,17,0)
		return out.value/256.0
	def getCHWaterPressure(self):
		out = self.doOTUntilIDMatch(0,18,0)
		return out.value/256.0
	def getDHWFlowRate(self):
		out = self.doOTUntilIDMatch(0,19,0)
		return out.value/256.0
	def getBoilerWaterTemp(self):
		out = self.doOTUntilIDMatch(0,25,0)
		return out.value/256.0
	def getDHWTemp(self):
		out = self.doOTUntilIDMatch(0,26,0)
		return out.value/256.0
	def getOutsideTemp(self):
		out = self.doOTUntilIDMatch(0,27,0)
		return out.value/256.0
	def getReturnTemp(self):
		out = self.doOTUntilIDMatch(0,28,0)
		return out.value/256.0
	def getSolarStorageTemp(self):
		out = self.doOTUntilIDMatch(0,29,0)
		return out.value/256.0
	def getSolarCollectorTemp(self):
		out = self.doOTUntilIDMatch(0,30,0)
		return out.value
	def getFlowTempCH2(self):
		out = self.doOTUntilIDMatch(0,31,0)
		return out.value/256.0
	def getDHW2Temp(self):
		out = self.doOTUntilIDMatch(0,32,0)
		return out.value/256.0
	def getExhaustTemp(self):
		out = self.doOTUntilIDMatch(0,33,0)
		return out.value
	def getBurnerStarts(self):
		out = self.doOTUntilIDMatch(0,116,0)
		return out.value
	def getCHPumpStarts(self):
		out = self.doOTUntilIDMatch(0,117,0)
		return out.value
	def getDHWPumpStarts(self):
		out = self.doOTUntilIDMatch(0,118,0)
		return out.value
	def getDHWBurnerStarts(self):
		out = self.doOTUntilIDMatch(0,119,0)
		return out.value
	def getBurnerOperationHours(self):
		out = self.doOTUntilIDMatch(0,120,0)
		return out.value
	def getCHPumpOperationHours(self):
		out = self.doOTUntilIDMatch(0,121,0)
		return out.value
	def getDHWPumpOperationHours(self):
		out = self.doOTUntilIDMatch(0,122,0)
		return out.value
	def getDHWBurnerOperationHours(self):
		out = self.doOTUntilIDMatch(0,123,0)
		return out.value
	#end sensors
	def setGetMAXTemp(self,temp=0):
		if temp==0:
			out = self.doOTUntilIDMatch(0,57,0)
		else:
			out = self.doOTUntilIDMatch(1,57,temp*256)
		if out.id!=57:
			return False
		return out.value/256.0
	def setTempCH2(self,temp):
		out = self.OT(1,8,temp*256)
		if out.id!=1:
			out.error = 1
			return out
		return out.value/256.0
	def setRoomTargetTemp(self,temp):
		out = self.OT(1,16,temp*256)
		if out.id!=1:
			out.error = 1
			return out
		return out.value/256.0
	def setRoomTargetTempCH2(self,temp):
		out = self.OT(1,23,temp*256)
		if out.id!=1:
			out.error = 1
			return out
		return out.value/256.0
	def setRoomTemp(self,temp):
		out = self.OT(1,24,temp*256)
		if out.id!=1:
			out.error = 1
			return out
		return out.value/256.0
	def getTemp(self):
		d = self.sendReceive(self.RPi_GET_HW_TEMP_UART_ADDRESS,0,0,0)
		if self.addressMatchError>0:
			self.addressMatchError=0
			return None
		return	((d>>16)&0xFFFF)/256.0
	def getOTStatus(self):
		#self.otStatus = self.getOpenTermStatus(6)
		#self.boilerStatus = self.getBoilerReg(0)
		#self.boilerConfig = self.getBoilerReg(3)
		#self.errorFlags = self.getBoilerReg(5)
		out = self.doOTUntilIDMatch(0,0,2<<8)
		#if out.type is 4:
		self.boilerStatus = out.value
		#print("accepted")
		time.sleep(0.1)
		
		out = self.doOTUntilIDMatch(0,3,0)
		#if out.type is 4:
			#print("accepted")
		self.boilerConfig = out.value
		time.sleep(0.1)
		out = self.doOTUntilIDMatch(0,5,0)
		#if out.type is 4:
		#	print("accepted")
		self.errorFlags = out.value
		self.otData = OTData(self.otStatus,self.boilerStatus,self.boilerConfig,self.errorFlags)
		return	self.otData
	def getADC(self,ch):
		d = self.sendReceive(self.RPi_ADC_UART_ADDRESS,ch,0,0)
		if self.addressMatchError>0:
			self.addressMatchError=0
			return None
		return ((d>>16)&0xFFFF)/256.0
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