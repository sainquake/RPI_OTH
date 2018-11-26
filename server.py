#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler,HTTPServer
import shutil
import sys
from OpenThermHat import OpenThermHat,OTData
import time
import json
from urllib.parse import urlparse,parse_qs

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
		
		parsed_path = urlparse(self.path).path
		#self.wfile.write( parsed_path.encode() )
		
		query_components = parse_qs(urlparse(self.path).query)
		#self.wfile.write( json.dumps(query_components).encode() )
		if parsed_path=="/hello":
			self.wfile.write( str("hello").encode() )
		if parsed_path=="/json":
			self.wfile.write( json.dumps(oth.otData.__dict__).encode() )
		if parsed_path=="/echo":
			echo = oth.sendReceive(OpenThermHat.RPi_ECHO_UART_ADDRESS,0,int(query_components["d"][0])&0xFF,(int(query_components["d"][0])>>8)&0xFF)
			#print( query_components["d1"][0] )
			self.wfile.write( json.dumps({ "echo": (echo>>16)&0xFFFF}).encode() )
		if parsed_path=="/otstatus":
			oth.otStatus = oth.getOpenTermStatus(6)
			oth.otData = OTData(oth.otStatus,oth.boilerStatus,oth.boilerConfig,oth.errorFlags)
			self.wfile.write( json.dumps(oth.otData.__dict__).encode() )
		if parsed_path=="/otstatusweb":
			oth.otStatus = oth.getOpenTermStatus(6)
			oth.otData = OTData(oth.otStatus,oth.boilerStatus,oth.boilerConfig,oth.errorFlags)
			#self.wfile.write( json.dumps(oth.otData.__dict__).encode() )
			
			f = open('html.html', 'r')
			self.wfile.write( f.read().encode() )
			f.close()
			
			for key, value in oth.otData.__dict__.items():
				self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>"+str(key)+":"+str(value)+"C</p></div></div><hr>").encode() )
			
			
			f = open('footer.html', 'r')
			self.wfile.write( f.read().encode() )
			f.close()
		if parsed_path=="/otreq":
			#oth.getOpenTermStatus(7)
			resp = oth.getBoilerReg(int(query_components["r"][0]))
			print( int(query_components["r"][0]) )
			print( resp )
			self.wfile.write( json.dumps({ "resp": resp}).encode() )
		if parsed_path=="/otreset":
			oth.getOpenTermStatus(7)
			self.wfile.write( json.dumps(oth.otData.__dict__).encode() )
		if parsed_path=="/ot":
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
