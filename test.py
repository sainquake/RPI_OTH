#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from OpenThermHat import OpenThermHat
import time
import json

oth = OpenThermHat()


lastSMSNum = 1
boilerSwitchedOff = 1
gsmModuleOff = 1

while True:
	if not oth.isEnabled():
		oth.resetMCU()
		print("RESET MCU")
		time.sleep(1)
		if not oth.isEnabled():
			print("MCU not working;terminatу; send sms about it")
			break	
	print("(DS18B20) indorTemp=\t"+str(oth.getTemp()))
	print("(Vin) Ubat Voltage=\t"+str(oth.getADC(7)))
	print("(RPi_3V3) 3v3 Voltage=\t"+str(oth.getADC(5)))
	print("(4v) GSM Voltage=\t"+str(oth.getADC(4)))
	print("(5v) USB Voltage=\t"+str(oth.getADC(6)))
	if not oth.isOTEnabled():
		print("Boiler is not enabled; check powering or opentherm connection wire")
		#time.sleep(0.3)
		break
		
	oth.getOTStatus()
	oth.otData.printClass()
	
	print( "============================" )
	print( "CH mode" if oth.otData.boilerCHMode else None )
	print( "DHW mode" if oth.otData.boilerDHWMode else None )
	print( "Flame ON" if oth.otData.boilerFlameStatus else "Flame OFF" )
	print( "!!!Fault!!!" if oth.otData.boilerFault else None )
	print( "============================" )
	
	print("set temperature=\t"+str(oth.setTemp(52)))
	print("set DHW temperature=\t"+str(oth.setDHWTemp(40)))
	print("set MAX temperature=\t"+str(oth.setGetMAXTemp(70)))
	print("get MAX temperature=\t"+str(oth.setGetMAXTemp()))
	
	print("set setRoomTargetTemp=\t"+str(oth.setRoomTargetTemp(30)))
	print("set setRoomTemp=\t"+str(oth.setRoomTemp(30)))
	
	
	break

time.sleep(500)





















#print("fff"+str(None))
while True:
	echo = oth.sendReceive(OpenThermHat.RPi_ECHO_UART_ADDRESS,0,4,5)
	#if echo[]
	if (echo>>16)&0xFFFF!=0x0504:
		oth.resetMCU()
		print("RESET MCU")
	time.sleep(0.5)
	print(str(oth.setTemp(52)))
	time.sleep(0.5)	
	print("indorTemp=\t"+str(oth.getTemp()))
	time.sleep(0.5)	
	print ("USB Voltage=\t"+str(oth.getADC(6)))
	#time.sleep(0.5)
	#print("BoilerID=\t"+str(oth.getBoilerID()))
	time.sleep(0.5)
	boilerSwitchedOff = oth.getOpenTermStatus(0)
	print("BoilerSwitchedOff=\t"+str(boilerSwitchedOff))
#	if boilerSwitchedOff==0:
	time.sleep(0.5)
	print("BoilerID=\t"+str(oth.getBoilerID()))
	time.sleep(0.5)
	print("hardware id=\t"+str(oth.getMem(0)))
	time.sleep(0.5)
	gsmModuleOff = oth.getGSM(255)
	print("GSM module off\t"+str(gsmModuleOff))
	if gsmModuleOff==0:
		time.sleep(0.5)
		print("GSM module (AT) enabled=\t"+str(oth.getGSM(0)))
		time.sleep(0.5)
		print("GSM module (AT+CPIN) SIM inserted=\t"+str(oth.getGSM(9)))
		time.sleep(0.5)
		print("GSM module (AT+CSQ) network quality (>10 is good)=\t"+str(oth.getGSM(21)))
		time.sleep(0.5)
		print("GSM module (AT+CBC) battery voltage(mV)=\t"+str(oth.getGSM(23)))
		time.sleep(0.5)
		print("GSM operator:"+str(oth.getOperator()))
		time.sleep(0.5)
		#if oth.getGSM(8,2)!=1: #balance received
		#	time.sleep(0.5)
		#	print("GSM balance request:"+str(oth.getGSM(8,1)))
		time.sleep(0.5)
		print("GSM balance:"+str(oth.getGSM(8)))
		time.sleep(0.5)
		lastSMSNum = oth.getGSM(25)
		if lastSMSNum>60:
			lastSMSNum=1
		print("GSM smsCount:"+str(lastSMSNum))
		time.sleep(0.5)
		print("GSM set smsToRead")
		oth.getSMS(lastSMSNum)
		time.sleep(1)
		sms = oth.getSMS(0)
		if len(sms)>3:
			print("GSM read sms phone number:"+str(sms[0])+"\t text:"+str(sms[1]))

