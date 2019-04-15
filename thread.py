#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from OpenThermHat import OpenThermHat
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
		self.setTemp = 60
		self.setDHWTemp = 40
		self.getDHWTemp = 0
		self.RelativeModulationLevel=0
		self.ReturnTemp = 0
oth = OpenThermHat()
p = Parameters()
i = 0
def init():
	if not oth.isEnabled():
		oth.resetMCU()
		print("RESET MCU")
		time.sleep(1)
		if not oth.isEnabled():
			print("MCU not working;terminatу; send sms about it")
	print("(DS18B20) indorTemp=\t"+str(oth.getTemp()))
	print("(Vin) Ubat Voltage=\t"+str(oth.getADC(7)))
	print("(RPi_3V3) 3v3 Voltage=\t"+str(oth.getADC(5)))
	print("(4v) GSM Voltage=\t"+str(oth.getADC(4)))
	print("(5v) USB Voltage=\t"+str(oth.getADC(6)))
	if not oth.isOTEnabled():
		print("Boiler is not enabled; check powering or opentherm connection wire")
def loop():
	print(i)
	
	oth.setOTStatus(3)
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
	p.Vin = oth.getADC(7)
	p.RPi_3V3 = oth.getADC(5)
	p.v4 = oth.getADC(4)
	p.v5 = oth.getADC(6)
	threading.Timer(1.0, loop).start()
	

class myHandler(BaseHTTPRequestHandler):
	#Handler for the GET requests
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		# Send the html message
		#self.wfile.write(("hello").encode() )
		#self.wfile.write(("<p>You accessed path: %s</p>" % self.path).encode())
		#do blink
		query_components = parse_qs(urlparse(self.path).query)
		parsed_path = urlparse(self.path).path
		if parsed_path=="/set"
			p.setTemp = int(query_components["temp"][0])
		if parsed_path=="/mode":
			global oth
			global p
			self.wfile.write(('<html><head><title></title><meta http-equiv="refresh" content="3"></head><body>' ).encode() )
			self.wfile.write(( "CH mode ON</p>" if oth.otData.boilerCHMode else "CH mode OFF</p>" ).encode() )
			self.wfile.write(( "DHW mode ON</p>" if oth.otData.boilerDHWMode else "DHW mode OFF</p>" ).encode() )
			self.wfile.write(( "Flame ON</p>" if oth.otData.boilerFlameStatus else "Flame OFF</p>" ).encode() )
			self.wfile.write(( "</p>" ).encode() )
			self.wfile.write(( "setTemp=\t"+str(p.setTemp)+"</p>" ).encode() )
			self.wfile.write(( "setDHWTemp=\t"+str(p.setDHWTemp)+"</p>" ).encode() )
			self.wfile.write(( "RelativeModulationLevel=\t"+str(p.RelativeModulationLevel)+"</p>" ).encode() )
			self.wfile.write(( "</p>" ).encode() )
			self.wfile.write(( "ReturnTemp=\t"+str(p.ReturnTemp)+"</p>" ).encode() )
			self.wfile.write(( "</p>" ).encode() )
			self.wfile.write(( "(DS18B20) indorTemp=\t"+str(p.indorTemp)+"</p>" ).encode() )
			self.wfile.write(( "(Vin) Ubat Voltage=\t"+str(p.Vin)+"</p>").encode() )
			self.wfile.write(( "(RPi_3V3) 3v3 Voltage=\t"+str(p.RPi_3V3)+"</p>").encode() )
			self.wfile.write(( "(4v) GSM Voltage=\t"+str(p.v4)+"</p>").encode() )
			self.wfile.write(( "(5v) USB Voltage=\t"+str(p.v5)+"</p>").encode() )
			self.wfile.write(('</body></html>' ).encode() )
		return

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print( 'Started httpserver on port ' , PORT_NUMBER)
	
	#Wait forever for incoming htto requests
	
	#if __name__ == '__main__':
	init()
	loop()
	server.serve_forever()
	#Thread(target = server.serve_forever).start()
		#Thread(target = loop).start()
		
except KeyboardInterrupt:
	print( '^C received, shutting down the web server')
	server.socket.close()