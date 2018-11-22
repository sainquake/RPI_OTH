#!/usr/bin/env python3

import serial
import time
import binascii

class GSM:
	def __init__(self):
		print("init /dev/ttyUSB0")
		self.ser = serial.Serial("/dev/ttyUSB0")
		self.ser.baudrate = 9600
		self.ser.timeout = 2
	def sendReceive(self, data,delay=0):
		self.ser.write(data.encode())
		if delay>0:
			time.sleep(delay)
		result = self.ser.readlines()
		return result
	def getSMSCount(self):
		req = self.sendReceive("AT+CPMS?\r\n")
		return str(req[1],'ascii').split(',')[1]
	def readLastSMS(self):
		lastSMSNumber = self.getSMSCount()
		req = self.sendReceive("AT+CMGR="+lastSMSNumber+"\r\n")
		return str(req[2],'ascii')
	def close(self):
		self.ser.close()
		
		
gsm = GSM()

try:

	#while True:
	req = gsm.sendReceive("AT\r\n")
	print(str(req[0],'ascii'))
	print(str(req[1],'ascii'))
	
	print(gsm.readLastSMS() )
	
	print(gsm.sendReceive("ATI\r\n"))
	print(gsm.sendReceive("AT+CSQ\r\n"))
	print(gsm.sendReceive("AT+GSN\r\n"))
	print(gsm.sendReceive("AT+CBC\r\n"))
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
