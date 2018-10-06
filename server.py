#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler,HTTPServer
import shutil
import sys

PORT_NUMBER = 8080

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type'.encode(),'text/html'.encode())
		self.end_headers()
		# Send the html message
		#self.wfile.write("Hello World !".encode())
		#self.wfile.write(("<p>You accessed path: " +str(self.path)+ "</p>").encode() )
		f = open('html.html', 'r')
		self.wfile.write( f.read().encode() )
		f.close()
		
		self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'>").encode() )
		self.wfile.write(("<p>temp: 88</p>").encode() )
		self.wfile.write(("</div></div><hr>").encode() )
  
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
