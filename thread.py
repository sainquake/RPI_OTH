#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from OpenThermHat import OpenThermHat
from OpenThermHat import GSM
from OpenThermHat import WS281X
from http.server import BaseHTTPRequestHandler,HTTPServer
import threading
from threading import Thread
import time
from urllib.parse import urlparse,parse_qs
PORT_NUMBER = 8080

class Parameters:
	def __init__(self):
		self.indorTemp = 0
		self.Vin = 0
		self.RPi_3V3 = 0
		self.v4 = 0
		self.v5 = 0
		self.enableOTCommunicationInLoop = False
		self.setTemp = 60
		self.setDHWTemp = 40
		self.DHWTemp = 0
		self.DHWFlowRate = 0
		self.RelativeModulationLevel=0
		self.ReturnTemp = 0
		self.isOTEnabled = False
		self.balanceRequered = False
		self.sendSMSRequest = False
oth = OpenThermHat()
gsm = GSM()
led = WS281X() 
p = Parameters()
i = 0
def init():
	led.set(0,(20,0,0))
	if not oth.isEnabled():
		oth.resetMCU()
		led.set(0,(255,0,0))
		print("RESET MCU")
		time.sleep(1)
		if not oth.isEnabled():
			led.set(0,(255,0,255))
			print("MCU not working;terminatу; send sms about it")
	led.set(0,(0,255,0))
	print("(DS18B20) indorTemp=\t"+str(oth.getTemp()))
	print("(Vin) Ubat Voltage=\t"+str(oth.getADC(7)))
	print("(RPi_3V3) 3v3 Voltage=\t"+str(oth.getADC(5)))
	print("(4v) GSM Voltage=\t"+str(oth.getADC(4)))
	print("(5v) USB Voltage=\t"+str(oth.getADC(6)))
	led.set(0,(200,200,200))
def loop():
	#print(i)
	if p.enableOTCommunicationInLoop:
		p.isOTEnabled = oth.isOTEnabled()
		if not p.isOTEnabled:
			print("Boiler is not enabled; check powering or opentherm connection wire")
		print( "ERROR" if oth.setOTStatus(3).error>0 else "OK" )
		print( "============================" )
		if oth.otData.boilerFault:
			print( "!!!Fault!!!")
		else:
			print( "CH mode ON" if oth.otData.boilerCHMode else "CH mode OFF" )
			print( "DHW mode ON" if oth.otData.boilerDHWMode else "DHW mode OFF" )
			print( "Flame ON" if oth.otData.boilerFlameStatus else "Flame OFF" )
		print( "============================" )
		print("set DHW temperature=\t"+str(oth.setDHWTemp(p.setDHWTemp)))
		print("set temperature=\t"+str(oth.setTemp(p.setTemp)))
		
		p.RelativeModulationLevel = oth.getRelativeModulationLevel()
		p.ReturnTemp = oth.getReturnTemp()
		p.indorTemp = oth.getTemp()
		p.DHWTemp = oth.getDHWTemp()
		p.DHWFlowRate = oth.getDHWFlowRate()
	p.Vin = oth.getADC(7)
	p.RPi_3V3 = oth.getADC(5)
	p.v4 = oth.getADC(4)
	p.v5 = oth.getADC(6)
	threading.Timer(1.0, loop).start()
def initGSM():
	led.set(1,(20,0,0))
	if not gsm.isEnabled():
		print("need to reset")
		print("GSM not working;terminate")
		#quit()
	else:
		led.set(1,(0,0,100))
		print("module enabled "+str(True))
	if not gsm.isSIMInserted():
		print("sim is not inserted; reset")
		gsm.softwareReset()
		if not gsm.isSIMInserted():
			led.set(1,(200,0,0))
			print("sim is not inserted; terminate")
			#quit()
	else:
		led.set(1,(1,100,100))
	#print("reset:"+str(gsm.softwareReset()) )
	print("fun:"+str(gsm.getPhoneFunctionality()) )
	led.set(1,(50,100,100))
	print("isSIMInserted:"+str(gsm.isSIMInserted()) )
	print("getCOPS:"+str(gsm.getCOPS()) )
	print("getPhoneActivityStatus:"+str(gsm.getPhoneActivityStatus()) )
	led.set(1,(75,100,100))
	
	#print("last sms:"+str(gsm.readLastSMS()) )
	print(gsm.getUnicNumber() )
	#print("charge "+str(gsm.getBatteryCharge())+"%" )
	#print("charge "+str(gsm.getBatteryVoltage())+"V" )
	#print("signal quality "+ str(gsm.getSignalQuality())+"/31")
	led.set(1,(100,100,100))
	#print("operator "+gsm.getOperator())
	led.set(1,(200,200,200))
	#gsm.deleteAllSMS()
def gsmLoop():
	if gsm.isEnabled():
		gsm.getUnicNumber()
		gsm.getBatteryCharge()
		gsm.getBatteryVoltage()
		gsm.getSignalQuality()
		if gsm.isSIMInserted():
			if p.balanceRequered:
				print("!!!!!!!!!!!!!!!!!!!!balance!!!!!!!!!!!!!!")
				p.balanceRequered = False
				gsm.getBalance()
			if p.sendSMSRequest:
				print("!!!!!!!!!!!!!!!!!!!!sms!!!!!!!!!!!!!!")
				p.sendSMSRequest = False
				gsm.sendSMS()
			gsm.getOperator()
	threading.Timer(5.5, gsmLoop).start()

class myHandler(BaseHTTPRequestHandler):
	#Handler for the GET requests
	def do_GET(self):
		global oth
		global p
		global gsm
		global led
		
		led.set(3,(0,0,200))
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		# Send the html message
		#self.wfile.write(("hello").encode() )
		#self.wfile.write(("<p>You accessed path: %s</p>" % self.path).encode())
		#do blink
		query_components = parse_qs(urlparse(self.path).query)
		
		print (query_components)
		parsed_path = urlparse(self.path).path
		if parsed_path=="/set":
			p.setTemp = int(query_components["temp"][0])
		if parsed_path=="/setDHW":
			p.setDHWTemp = int(query_components["temp"][0])
		if parsed_path=="/enable":
			p.enableOTCommunicationInLoop = True
		if parsed_path=="/disable":
			p.enableOTCommunicationInLoop = False
		#GSM
		if parsed_path=="/balance":
			p.balanceRequered = True
			self.wfile.write(( "gsm balance=\t"+str(gsm.balance)+"</p>").encode() )
		if parsed_path=="/sendSMS":
			gsm.smsNumber = str(query_components["smsNumber"][0])
			gsm.smsMessage = str(query_components["smsMessage"][0])
			p.sendSMSRequest = True
			self.wfile.write(( "gsm send SMS</p>").encode() )
		
		#
		if parsed_path=="/show":

			self.wfile.write(('<html><head><title></title><meta http-equiv="refresh" content="3"></head><body>' ).encode() )
			self.wfile.write(( "isOTEnabled=\t"+str(p.isOTEnabled)+"</p>" ).encode() )
			self.wfile.write(( "CH mode ON</p>" if oth.otData.boilerCHMode else "CH mode OFF</p>" ).encode() )
			self.wfile.write(( "DHW mode ON</p>" if oth.otData.boilerDHWMode else "DHW mode OFF</p>" ).encode() )
			self.wfile.write(( "Flame ON</p>" if oth.otData.boilerFlameStatus else "Flame OFF</p>" ).encode() )
			self.wfile.write(( "</p>" ).encode() )
			self.wfile.write(( "setTemp=\t"+str(p.setTemp)+"</p>" ).encode() )
			self.wfile.write(( "setDHWTemp=\t"+str(p.setDHWTemp)+"</p>" ).encode() )
			self.wfile.write(( "RelativeModulationLevel=\t"+str(p.RelativeModulationLevel)+"</p>" ).encode() )
			self.wfile.write(( "DHWTemp=\t"+str( p.DHWTemp)+"</p>" ).encode() ) 
			self.wfile.write(( "ReturnTemp=\t"+str(p.ReturnTemp)+"</p>" ).encode() )
			self.wfile.write(( "DHWFlowRate=\t"+str(p.DHWFlowRate)+"</p>" ).encode() ) 
			self.wfile.write(( "(DS18B20) indorTemp=\t"+str(p.indorTemp)+"</p>" ).encode() )
			self.wfile.write(( "(Vin) Ubat Voltage=\t"+str(p.Vin)+"</p>").encode() )
			self.wfile.write(( "(RPi_3V3) 3v3 Voltage=\t"+str(p.RPi_3V3)+"</p>").encode() )
			self.wfile.write(( "(4v) GSM Voltage=\t"+str(p.v4)+"</p>").encode() )
			self.wfile.write(( "(5v) USB Voltage=\t"+str(p.v5)+"</p>").encode() )
			
			self.wfile.write(( "gsm enabled=\t"+str(gsm.OK)+"</p>").encode() )
			self.wfile.write(( "gsm SIMInserted=\t"+str(gsm.SIMInserted)+"</p>").encode() )
			self.wfile.write(( "gsm unicNumber=\t"+str(gsm.unicNumber)+"</p>").encode() )
			self.wfile.write(( "gsm batteryCharge=\t"+str(gsm.batteryCharge)+"</p>").encode() )
			self.wfile.write(( "gsm batteryVoltage=\t"+str(gsm.batteryVoltage)+"</p>").encode() )
			self.wfile.write(( "gsm signalQuality=\t"+str(gsm.signalQuality)+"</p>").encode() )
			self.wfile.write(( "gsm operator=\t"+str(gsm.operator)+"</p>").encode() )
			self.wfile.write(( "gsm balance=\t"+str(gsm.balance)+"</p>").encode() )
			self.wfile.write(( "gsm lastSMS=\t"+str(gsm.lastSMS)+"</p>").encode() )
			self.wfile.write(('</body></html>' ).encode() )
		led.set(3,(0,0,0))
		return

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print( 'Started httpserver on port ' , PORT_NUMBER)
	
	#Wait forever for incoming htto requests
	
	#if __name__ == '__main__':
	#led.fill((0,0,0))
	for i in range(100):
		led.percent(i/100)
		time.sleep(0.1)
	init()
	initGSM()
	loop()
	gsmLoop()
	led.set(2,(200,200,200))
	server.serve_forever()
	
	#Thread(target = server.serve_forever).start()
		#Thread(target = loop).start()
		
except KeyboardInterrupt:
	print( '^C received, shutting down the web server')
	server.socket.close()