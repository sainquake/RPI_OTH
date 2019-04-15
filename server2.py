#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler,HTTPServer
import threading
from threading import Thread
import time
PORT_NUMBER = 8080

i = 0
def loop():
	print(i)
	threading.Timer(1.0, loop).start()
class myHandler(BaseHTTPRequestHandler):
	#Handler for the GET requests
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		# Send the html message
		self.wfile.write(("hello").encode() )
		self.wfile.write(("<p>You accessed path: %s</p>" % self.path).encode())
		#do blink
		if self.path=="/blink":
			global i
			print(i)
			i=i+1
		return

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print( 'Started httpserver on port ' , PORT_NUMBER)
	
	#Wait forever for incoming htto requests
	#server.serve_forever()
	#if __name__ == '__main__':
	loop()
	Thread(target = server.serve_forever).start()
		#Thread(target = loop).start()
		
except KeyboardInterrupt:
	print( '^C received, shutting down the web server')
	server.socket.close()