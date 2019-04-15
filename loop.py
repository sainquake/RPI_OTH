#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#chmod +x loop.python3
from OpenThermHat import OpenThermHat
import time
import json
import sys
import datetime

class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("logfile.log", "a", encoding='utf8')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)  

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass    

sys.stdout = Logger()

if len(sys.argv)>1:
	check_link = sys.argv[1] 
else:
	check_link = ""
today = datetime.date.today()

print (sys.argv[0])
print (today)

oth = OpenThermHat()

try:
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
	
	while True:	
		#oth.isOTEnabled()
		#print( "OTStatus OK" if oth.getOTStatus() else None ) 
		oth.setOTStatus(3)
		print( "============================" )
		if oth.otData.boilerFault:
			print( "!!!Fault!!!")
		else:
			print( "CH mode ON" if oth.otData.boilerCHMode else "CH mode OFF" )
			print( "DHW mode ON" if oth.otData.boilerDHWMode else "DHW mode OFF" )
			print( "Flame ON" if oth.otData.boilerFlameStatus else "Flame OFF" )
		print( "============================" )
		print("set DHW temperature=\t"+str(oth.setDHWTemp(40)))
		print("set temperature=\t"+str(oth.setTemp(60)))
		time.sleep(1)
except KeyboardInterrupt:
	print( '! ^C received, shutting down')
	gsm.close()
print ("terminate")