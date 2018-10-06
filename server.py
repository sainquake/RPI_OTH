#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler,HTTPServer

PORT_NUMBER = 8080

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type','text/html'.encode())
		self.end_headers()
		# Send the html message
		self.wfile.write("Hello World !".encode())
		self.wfile.write(("<p>You accessed path: " +str(self.path)+ "</p>").encode() )
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
