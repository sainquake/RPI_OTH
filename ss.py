#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler,HTTPServer
import shutil
import sys
import binascii
import time
import json
from urllib.parse import urlparse,parse_qs
import serial

PORT_NUMBER = 8080

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
			#self.wfile.write( str("hello").encode() )
			
			tx = binascii.unhexlify(query_components["tx"][0]).decode('utf8')
			
			#self.wfile.write( str( binascii.hexlify(tx.encode()) ).encode() )
			
			self.wfile.write( str( sendReceive(tx) ).encode() )
			
		if parsed_path=="/json":
			self.wfile.write( json.dumps(oth.otData.__dict__).encode() )
		if parsed_path=="/echo":
			echo = oth.sendReceive(OpenThermHat.RPi_ECHO_UART_ADDRESS,0,int(query_components["d"][0])&0xFF,(int(query_components["d"][0])>>8)&0xFF)
			#print( query_components["d1"][0] )
			self.wfile.write( json.dumps({ "echo": (echo>>16)&0xFFFF}).encode() )
		
		return

def sendReceive( data,delay=0):
	ser.write(data.encode())
	if delay>0:
		time.sleep(delay)
	result = ser.readlines()
	return result
		
try:	
	print("init /dev/ttyUSB0")
	ser = serial.Serial("/dev/ttyUSB0")
	ser.baudrate = 9600
	ser.timeout = 2
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print( 'Started httpserver on port ' , PORT_NUMBER)
	
	#Wait forever for incoming htto requests
	server.serve_forever()
	
		

except KeyboardInterrupt:
	print( '^C received, shutting down the web server')
	server.socket.close()
