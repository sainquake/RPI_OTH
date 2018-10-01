#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from OpenThermHat import OpenThermHat
import time

oth = OpenThermHat()
oth.resetMCU()

lastSMSNum = 1
boilerSwitchedOff = 1
gsmModuleOff = 1

#print("fff"+str(None))
while True:
	echo = oth.sendReceive(OpenThermHat.RPi_ECHO_UART_ADDRESS,0,4,5)
	#if echo[]
	if (echo>>16)&0xFFFF!=0x0504:
		oth.resetMCU()
		print("RESET MCU")
	time.sleep(0.5)
	oth.setTemp(52)
	time.sleep(0.5)	
	print("indorTemp=\t"+str(oth.getTemp()))
	time.sleep(0.5)	
	print ("USB Voltage=\t"+str(oth.getADC(6)))
	#time.sleep(0.5)
	#print("BoilerID=\t"+str(oth.getBoilerID()))
	time.sleep(0.5)
	boilerSwitchedOff = oth.getOpenTermStatus(0)
	print("BoilerSwitchedOff=\t"+str(boilerSwitchedOff))
	if boilerSwitchedOff==0:
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

