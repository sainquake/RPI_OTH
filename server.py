#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler,HTTPServer
import shutil
import sys
from OpenThermHat import OpenThermHat
import time

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
		
		
		f = open('html.html', 'r')
		self.wfile.write( f.read().encode() )
		f.close()
		if self.path=="/ot":
			oth.getOTStatus()
			self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>'ot.timeout=\t'"+str(oth.otData.otTimeout)+"</p></div></div><hr>").encode() )
			self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>'ot.otIndex=\t'"+str(oth.otData.otIndex)+"</p></div></div><hr>").encode() )
			self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>'ot.otBusy=\t'"+str(oth.otData.otBusy)+"</p></div></div><hr>").encode() )
			self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>'ot.otComplete=\t'"+str(oth.otData.otComplete)+"</p></div></div><hr>").encode() )
			self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>'ot.otFrameSendedAndStartWaitingACK=\t'"+str(oth.otData.otFrameSendedAndStartWaitingACK)+"</p></div></div><hr>").encode() )
			self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>'ot.otReadingResponse=\t'"+str(oth.otData.otReadingResponse)+"</p></div></div><hr>").encode() )
			self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>'ot.otSpecialRequest=\t'"+str(oth.otData.otSpecialRequest)+"</p></div></div><hr>").encode() )
			self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>'ot.otSpecialRequestComplete=\t'"+str(oth.otData.otSpecialRequestComplete)+"</p></div></div><hr>").encode() )
			self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>'ot.otNoResponse=\t'"+str(oth.otData.otNoResponse)+"</p></div></div><hr>").encode() )	
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
