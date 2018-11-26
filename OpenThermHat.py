# -*- coding: utf-8 -*-
#!/usr/bin/env python3
#import binascii
import serial
import RPi.GPIO as GPIO
import time
import binascii
import re

print("OTH")

class GSM:
	def __init__(self):
		print("init /dev/ttyUSB0")
		self.ser = serial.Serial("/dev/ttyUSB0")
		self.ser.baudrate = 9600
		self.ser.timeout = 2
		self.OK = False
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
		return int(str(req[1],'ascii').split(',')[1])
	def readSMS(self,num):
		req = self.sendReceive("AT+CMGR="+str(num)+"\r\n")
		return str(req[2],'ascii')
	def readLastSMS(self):
		lastSMSNumber = str(self.getSMSCount())
		req = self.sendReceive("AT+CMGR="+lastSMSNumber+"\r\n")
		return str(req[2],'ascii')
	def deleteAllSMS(self):
		return self.sendReceive("AT+CMGDA=\"DEL ALL\"\r\n")
	def getUnicNumber(self):
		req = self.sendReceive("AT+GSN\r\n")
		return str(req[1],'ascii')
	def getBatteryCharge(self):
		req = self.sendReceive("AT+CBC\r\n")
		return int(str(req[1],'ascii').split(',')[1])
	def getBatteryVoltage(self):
		req = self.sendReceive("AT+CBC\r\n")
		return float(str(req[1],'ascii').split(',')[2])/1000
	def getBalance(self):
		req = self.sendReceive("AT+CUSD=1,\"#105#\"\r\n",20)
		sms = str(req[3],'ascii').split('"')
		try:
			req = binascii.unhexlify(sms[1]).decode('utf-16-be')
		except Exception:
			req = sms[1]
		return float(re.findall("\d+\.\d+", req)[0])
	def getOperator(self):
		req = self.sendReceive("AT+CSPN?\r\n")
		op = str(req[1],'ascii').split('"')[1]
		return str(op)
	def sendSMS(self,phone_number,message):
		req = self.sendReceive("AT+CMGF=1\r\n")
		if self.OK:
			req = self.sendReceive("AT+CMGS=\""+phone_number+"\"\r\n")
			if self.checkOK(req,">"):
				time.sleep(1)
				self.sendReceive(message)
				time.sleep(0.1)
				self.sendReceive("\x1a")
				self.sendReceive("AT\r\n")
				return self.OK
			else:
				return False
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
	def close(self):
		self.ser.close()
		
class OTResp:
	def __init__(self,type_,id_,value_,timeout_,complete_,whileBreak_):
		self.type = type_
		self.id = id_
		self.value = value_
		self.timeout = timeout_
		self.complete = complete_
		self.whileBreak = whileBreak_
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
		return (echo>>16)&0xFFFF is 0x0504
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
	def setTemp(self,temp):
		out = self.OT(1,1,temp*256)
		if out.id!=1:
			return False
		'''d = self.getBoilerReg((1<<7) +1,temp*256)/256.0
		if self.addressMatchError>0:
			self.addressMatchError=0
			return None'''
		return out.value/256.0
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
		#self.otStatus = self.getOpenTermStatus(6)
		#self.boilerStatus = self.getBoilerReg(0)
		#self.boilerConfig = self.getBoilerReg(3)
		#self.errorFlags = self.getBoilerReg(5)
		out = self.OT(0,0,0)
		if out.type is 4:
			self.boilerStatus = out.value
			print("accepted")
		time.sleep(0.1)
		
		out = self.OT(0,3,0)
		if out.type is 4:
			print("accepted")
			self.boilerConfig = out.value
		time.sleep(0.1)
		out = self.OT(0,5,0)
		if out.type is 4:
			print("accepted")
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