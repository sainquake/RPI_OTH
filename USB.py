#!/usr/bin/env python3

import serial
import time
import binascii
import re

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
	def initHTTP(self):
		print(self.sendReceive("AT+SAPBR=0,1\r\n",5))
		#print(gsm.sendReceive("AT+CSTT=\"ainternet.tele2.ru\",\"tele2\",\"tele2\"\r\n"))
		print(self.sendReceive("AT+SAPBR=3,1,\"CONTYPE\",\"GPRS\"\r\n"))
		print(self.sendReceive("AT+SAPBR=3,1,\"APN\",\"ainternet.tele2.ru\"\r\n"))
		print(self.sendReceive("AT+SAPBR=3,1,\"USER\",\"tele2\"\r\n"))
		print(self.sendReceive("AT+SAPBR=3,1,\"PWD\",\"tele2\"\r\n"))
		print(self.sendReceive("AT+SAPBR=1,1\r\n",5))
		
		print(self.sendReceive("AT+SAPBR=2,1\r\n"))
		
		print(self.sendReceive("AT+HTTPINIT\r\n",3))
		print(self.sendReceive("AT+HTTPPARA=\"CID\",1\r\n"))
	def HTTP(self,url):
		print(self.sendReceive("AT+HTTPPARA=\"URL\",\""+url+"\"\r\n"))
	
		print(self.sendReceive('AT+HTTPACTION=0\r\n',3))
		
	def checkOK(self,req,s="OK"):
		OK=False
		for member in req:
			if str(member,'ascii').find(s)>=0:
				OK=True
		return OK
	def close(self):
		self.ser.close()
		
		
gsm = GSM()

try:

	#while True:
	req = gsm.sendReceive("AT\r\n")
	print(req)
	print(gsm.OK)
	
	#time.sleep(100)
	#print(gsm.sendSMS("+79063280423","hello lash time"))
	'''
	req = gsm.sendReceive("ATZ\r\n")
	print(req)
	print(gsm.OK)
	'''
	#init
	'''
	print(gsm.sendReceive("AT+SAPBR=0,1\r\n",5))
	#print(gsm.sendReceive("AT+CSTT=\"ainternet.tele2.ru\",\"tele2\",\"tele2\"\r\n"))
	print(gsm.sendReceive("AT+SAPBR=3,1,\"CONTYPE\",\"GPRS\"\r\n"))
	print(gsm.sendReceive("AT+SAPBR=3,1,\"APN\",\"ainternet.tele2.ru\"\r\n"))
	print(gsm.sendReceive("AT+SAPBR=3,1,\"USER\",\"tele2\"\r\n"))
	print(gsm.sendReceive("AT+SAPBR=3,1,\"PWD\",\"tele2\"\r\n"))
	print(gsm.sendReceive("AT+SAPBR=1,1\r\n",5))
	
	print(gsm.sendReceive("AT+SAPBR=2,1\r\n"))
	
	print(gsm.sendReceive("AT+HTTPINIT\r\n",3))
	print(gsm.sendReceive("AT+HTTPPARA=\"CID\",1\r\n"))
	'''
	#init end
	#gsm.initHTTP()
	print(gsm.sendReceive("AT+HTTPPARA=\"URL\",\"google.com\"\r\n"))
	
	print(gsm.sendReceive('AT+HTTPACTION=0\r\n',3))
	print(gsm.sendReceive('AT+HTTPACTION=0\r\n',3))
	print(gsm.sendReceive('AT+HTTPREAD\r\n',10))
	#print(gsm.sendReceive('AT+HTTPTERM\r\n'))
	
	'''
	print(gsm.sendReceive("AT+HTTPINIT\r\n"))
	print(gsm.sendReceive('AT+HTTPPARA="CID",1\r\n'))
	print(gsm.sendReceive('AT+HTTPPARA="URL","google.com"\r\n'))
	#print(gsm.sendReceive('AT+HTTPACTION=0\r\n'))
	i=0
	while i is not 200:
		req = gsm.sendReceive('AT+HTTPACTION=0\r\n')
		req = str(req[3],'ascii').split(',')[1]
		print(req)
		i = int(req)
		print(i==200)
		time.sleep(2)
	print(gsm.sendReceive('AT+HTTPREAD\r\n'))
	print(gsm.sendReceive('AT+HTTPTERM\r\n'))
	
	
	print(gsm.readLastSMS() )
	print(gsm.getUnicNumber() )
	print(gsm.getBatteryCharge() )
	'''
 
	print(gsm.getBalance())
	
	print("-------------------")
	time.sleep(200)	
	
	print(gsm.sendReceive("ATI\r\n"))
	print(gsm.sendReceive("AT+CSQ\r\n"))
	
	
	print(gsm.sendReceive("AT+CREG?\r\n"))
	#print(gsm.sendReceive("AT+COPS?\r\n"))
	#print(gsm.sendReceive("AT+COPN\r\n"))
	print(gsm.sendReceive("AT+CPAS\r\n"))
	print(gsm.sendReceive("AT+CSPN?\r\n"))
	print(gsm.sendReceive("AT+CMGF=1\r\n"))
	
	#print(gsm.sendReceive("AT+CMGDA=\"DEL ALL\"\r\n"))#delete sms
	req = gsm.sendReceive("AT+CPMS?\r\n")
	
	lastSMSNumber = str(req[1],'ascii').split(',')[1]
	print(lastSMSNumber)
	
	req = gsm.sendReceive("AT+CMGR="+lastSMSNumber+"\r\n")
	print(req)
	print(str(req[2],'ascii'))
	#print(binascii.unhexlify(req[2].split('\r\n')).decode('utf-16-be'))
	
	
	
	
	req = gsm.sendReceive("AT+CUSD=1,\"#105#\"\r\n",20)
	#print(len(req))
	#print(req)
	sms = str(req[3],'ascii').split('"')
	print(binascii.unhexlify(sms[1]).decode('utf-16-be'))
except KeyboardInterrupt:
	print( '! ^C received, shutting down')
	gsm.close()
