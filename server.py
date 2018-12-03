#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler,HTTPServer
import shutil
import sys
from OpenThermHat import OpenThermHat,OTData
import time
import json
from urllib.parse import urlparse,parse_qs
from OpenThermHat import GSM

gsm = GSM()
oth = OpenThermHat()
#oth.resetMCU()

PORT_NUMBER = 8080

'''
echo = oth.sendReceive(OpenThermHat.RPi_ECHO_UART_ADDRESS,0,4,5)
if (echo>>16)&0xFFFF!=0x0504:
	oth.resetMCU()
	print("RESET MCU")
	time.sleep(5)
	'''
	
#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def status(self):
		f = open('html.html', 'r')
		self.wfile.write( f.read().encode() )
		f.close()
		
		if not gsm.isEnabled():
			print("need to reset")
			self.addLine("GSM not working;terminate")
		else:
			self.addLine("GSM module enabled "+str(True))
			self.addLine("last sms:"+str(gsm.readLastSMS()) )
			self.addLine("unic "+gsm.getUnicNumber() )
			self.addLine("charge "+str(gsm.getBatteryCharge())+"%" )
			self.addLine("charge "+str(gsm.getBatteryVoltage())+"V" )
			self.addLine("signal quality "+ str(gsm.getSignalQuality())+"/31")
			
			self.addLine("operator "+gsm.getOperator())
		
		if not oth.isEnabled():
			oth.resetMCU()
			print("RESET MCU")
			time.sleep(1)
			if not oth.isEnabled():
				self.addLine("MCU not working;terminatу; send sms about it")
				#break	
		self.addLine("(DS18B20) indorTemp=\t"+str(oth.getTemp()))
		self.addLine("(Vin) Ubat Voltage=\t"+str(oth.getADC(7)))
		self.addLine("(RPi_3V3) 3v3 Voltage=\t"+str(oth.getADC(5)))
		self.addLine("(4v) GSM Voltage=\t"+str(oth.getADC(4)))
		self.addLine("(5v) USB Voltage=\t"+str(oth.getADC(6)))
		if not oth.isOTEnabled():
			self.addLine("Boiler is not enabled; check powering or opentherm connection wire")
			#time.sleep(0.3)
			#break
			
		oth.getOTStatus()
		oth.otData.printClass()
		
		self.addLine( "ID=" + str(oth.otData.boilerMemberID) )
		
		print( "============================" )
		print( "CH mode" if oth.otData.boilerCHMode else None )
		print( "DHW mode" if oth.otData.boilerDHWMode else None )
		print( "Flame ON" if oth.otData.boilerFlameStatus else "Flame OFF" )
		print( "!!!Fault!!!" if oth.otData.boilerFault else None )
		print( "============================" )
		if oth.otData.boilerCHMode:
			self.addLine("CH mode")
		if oth.otData.boilerDHWMode:
			self.addLine("DHW mode")
		if oth.otData.boilerFlameStatus:
			self.addLine("Flame ON")
		else:
			self.addLine("Flame OFF")
		if oth.otData.boilerFault:
			self.addLine("!!!Fault!!!")
		self.addLine("get MAX temperature="+str(oth.setGetMAXTemp()))
		
		self.addLine("getRelativeModulationLevel="+str(oth.getRelativeModulationLevel()))
		self.addLine("getCHWaterPressure="+str(oth.getCHWaterPressure()))
		self.addLine("getDHWFlowRate="+str(oth.getDHWFlowRate()))
		self.addLine("getBoilerWaterTemp="+str(oth.getBoilerWaterTemp()))
		self.addLine("getDHWTemp="+str(oth.getDHWTemp()))
		self.addLine("getReturnTemp="+str(oth.getReturnTemp()))
		self.addLine("getSolarStorageTemp="+str(oth.getSolarStorageTemp()))
		self.addLine("getSolarCollectorTemp="+str(oth.getSolarCollectorTemp()))
		self.addLine("getFlowTempCH2="+str(oth.getFlowTempCH2()))
		self.addLine("getDHW2Temp="+str(oth.getDHW2Temp()))
		self.addLine("getExhaustTemp="+str(oth.getExhaustTemp()))
		self.addLine("getBurnerStarts="+str(oth.getBurnerStarts()))
		self.addLine("getCHPumpStarts="+str(oth.getCHPumpStarts()))
		self.addLine("getDHWPumpStarts="+str(oth.getDHWPumpStarts()))
		self.addLine("getDHWBurnerStarts="+str(oth.getDHWBurnerStarts()))
		self.addLine("getBurnerOperationHours="+str(oth.getBurnerOperationHours()))
		self.addLine("getCHPumpOperationHours="+str(oth.getCHPumpOperationHours()))
		self.addLine("getDHWPumpOperationHours="+str(oth.getDHWPumpOperationHours()))
		self.addLine("getDHWBurnerOperationHours="+str(oth.getDHWBurnerOperationHours()))
		'''
		for key, value in oth.otData.__dict__.items():
			self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>"+str(key)+":"+str(value)+"C</p></div></div><hr>").encode() )
		'''
		
		f = open('footer.html', 'r')
		self.wfile.write( f.read().encode() )
		f.close()
	def addLine(self,s):
		self.wfile.write(("<div class='w3-cell-row w3-container'><div class='w3-cell'><p>"+s+"</p></div></div><hr>").encode() )
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
		if parsed_path=="/status":
			self.status()
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
