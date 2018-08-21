#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

import serial
import RPi.GPIO as GPIO
import time


# Use "logical" pin numbers
GPIO.setmode(GPIO.BCM)
# Disable "This channel is already in use" warnings
GPIO.setwarnings(False)

# Setup MCU POWER UP
GPIO.setup(17, GPIO.OUT)
GPIO.output(17, True)
#LEDS
GPIO.setup(4, GPIO.OUT)
GPIO.output(4, True)

GPIO.setup(27, GPIO.OUT)
GPIO.output(27, True)

GPIO.setup(6, GPIO.OUT)
GPIO.output(6, True)


PORT_NUMBER = 8080

ser = serial.Serial ("/dev/ttyAMA0")    #Open named port 
ser.baudrate = 115200                     #Set baud rate to 9600

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		# Send the html message
		self.wfile.write("Hello World !")
		self.wfile.write("<p>You accessed path: %s</p>" % self.path)
		#do blink
		if self.path=="/blink":
			time.sleep(0.1)
			GPIO.output(4,False)
			GPIO.output(27,False)
			GPIO.output(6,False)
			time.sleep(0.5)
			GPIO.output(4,True)
			time.sleep(0.5)
			GPIO.output(4,False)
			GPIO.output(27,True)
			time.sleep(0.5)
			GPIO.output(27,False)
			GPIO.output(6,True)
			time.sleep(0.5)
			GPIO.output(6,False)
		if self.path=="/blinkstm":
			ser.write("Hel")
		return

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
