#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler,HTTPServer
import shutil
import sys
from OpenThermHat import OpenThermHat
import time
import json
import urlparse

oth = OpenThermHat()
#oth.resetMCU()

PORT_NUMBER = 8080


echo = oth.sendReceive(OpenThermHat.RPi_ECHO_UART_ADDRESS,0,4,5)
if (echo>>16)&0xFFFF!=0x0504:
	oth.resetMCU()
	print("RESET MCU")
	time.sleep(5)
#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type'.encode(),'text/html'.encode())
		self.end_headers()
		# Send the html message
		parsed_path = urlparse.urlparse(self.path)
		self.wfile.write( json.dumps(parsed_path.__dict__).encode() )
		
		if self.path=="/json":
			self.wfile.write( json.dumps(oth.otData.__dict__).encode() )
		if self.path=="/echo":
			echo = oth.sendReceive(OpenThermHat.RPi_ECHO_UART_ADDRESS,0,4,5)
			if (echo>>16)&0xFFFF!=0x0504:
				oth.resetMCU()
				print("RESET MCU")
				oth.ledControl(oth.RED,False)
			else:
				oth.ledControl(oth.RED,True)
			self.wfile.write( json.dumps(echo.__dict__).encode() )
		if self.path=="/ot":
			f = open('html.html', 'r')
			self.wfile.write( f.read().encode() )
			f.close()
			self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>exhoust temperature:"+str(oth.getBoilerReg(33))+"C</p></div></div><hr>").encode() )
			self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>Relative Modulation Level:"+str(oth.getBoilerReg(17)/256.0)+"%</p></div></div><hr>").encode() )
			self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>Boiler water temp:"+str(oth.getBoilerReg(25)/256.0)+"C</p></div></div><hr>").encode() )
			self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>DHW temperature:"+str(oth.getBoilerReg(26)/256.0)+"C</p></div></div><hr>").encode() )
			self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>Return water temperature:"+str(oth.getBoilerReg(28)/256.0)+"C</p></div></div><hr>").encode() )
			self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>burner starts:"+str(oth.getBoilerReg(19))+"l/min</p></div></div><hr>").encode() )
			self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>flow:"+str(oth.getBoilerReg(116))+"l/min</p></div></div><hr>").encode() )
			oth.getOTStatus()
			self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>ot.timeout=\t"+str(oth.otData.otTimeout)+"</p></div></div><hr>").encode() )
			self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>ot.otIndex=\t"+str(oth.otData.otIndex)+"</p></div></div><hr>").encode() )
			self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>ot.otBusy=\t"+str(oth.otData.otBusy)+"</p></div></div><hr>").encode() )
			self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>ot.otComplete=\t"+str(oth.otData.otComplete)+"</p></div></div><hr>").encode() )
			self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>ot.otFrameSendedAndStartWaitingACK=\t"+str(oth.otData.otFrameSendedAndStartWaitingACK)+"</p></div></div><hr>").encode() )
			self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>ot.otReadingResponse=\t"+str(oth.otData.otReadingResponse)+"</p></div></div><hr>").encode() )
			self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>ot.otSpecialRequest=\t"+str(oth.otData.otSpecialRequest)+"</p></div></div><hr>").encode() )
			self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>ot.otSpecialRequestComplete=\t"+str(oth.otData.otSpecialRequestComplete)+"</p></div></div><hr>").encode() )
			self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>ot.otNoResponse=\t'"+str(oth.otData.otNoResponse)+"</p></div></div><hr>").encode() )
			
			self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>boilerFault: "+str(oth.otData.boilerFault)+"</p></div></div><hr>").encode() )
			self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>boilerCHMode: "+str(oth.otData.boilerCHMode)+"</p></div></div><hr>").encode() )
			self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>boilerDHWMode: "+str(oth.otData.boilerDHWMode)+"</p></div></div><hr>").encode() )
			self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>boilerFlameStatus: "+str(oth.otData.boilerFlameStatus)+"</p></div></div><hr>").encode() )
			self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>boilerCoolingStatus: "+str(oth.otData.boilerCoolingStatus)+"</p></div></div><hr>").encode() )
			self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>boilerCH2Mode: "+str(oth.otData.boilerCH2Mode)+"</p></div></div><hr>").encode() )
			self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>boilerDiagnostic: "+str(oth.otData.boilerDiagnostic)+"</p></div></div><hr>").encode() )
			
			self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>boilerMemberID: "+str(oth.otData.boilerMemberID)+"</p></div></div><hr>").encode() )
			self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>boilerDHWPresent: "+str(oth.otData.boilerDHWPresent)+"</p></div></div><hr>").encode() )
			self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>boilerControlType: "+str(oth.otData.boilerControlType)+"</p></div></div><hr>").encode() )
			self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>boilerCoolingConfig: "+str(oth.otData.boilerCoolingConfig)+"</p></div></div><hr>").encode() )
			self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>boilerDHWConfig: "+str(oth.otData.boilerDHWConfig)+"</p></div></div><hr>").encode() )
			self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>boilerPumpControlFunction: "+str(oth.otData.boilerPumpControlFunction)+"</p></div></div><hr>").encode() )
			
			self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>errorFlags: "+str(oth.errorFlags)+"</p></div></div><hr>").encode() )
			f = open('footer.html', 'r')
			self.wfile.write( f.read().encode() )
			f.close()
		return

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print( 'Started httpserver on port ' , PORT_NUMBER)
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print( '^C received, shutting down the web server')
	server.socket.close()
