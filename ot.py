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

	time.sleep(5)
	boilerStatus = oth.getOpenTermStatus(6)
	print(" ")
	print("ot.timeout=\t"+str(boilerStatus&1))
	print("ot.index=\t"+str(boilerStatus>>8&0xFF))
	print("ot.busy=\t"+str(boilerStatus>>1&1))
	print("ot.complete=\t"+str(boilerStatus>>2&1))
	print("ot.frameSendedAndStartWaitingACK=\t"+str(boilerStatus>>3&1))
	print("ot.readingResponse=\t"+str(boilerStatus>>4&1))
	print(" ")
	d = oth.getBoilerReg(3)
#	time.sleep(0.5)
	h = oth.getBoilerHeader(3)
	print("Boiler ID3=\t"+str(d) + " \theader" +str(hex(h))+"\t boiler id")
#	time.sleep(0.1)
	print("Boiler ID0=\t"+str(oth.getBoilerReg(0)) + "\t status")
#	time.sleep(0.1)
	print("Boiler ID5=\t"+str(oth.getBoilerReg(5)) + "\tflags")
#	time.sleep(0.5)
	#print("Boiler ID28=\t"+str(oth.getBoilerReg(28)/256.0)+"\tReturn water temperature")
	#time.sleep(0.1)
	print("Boiler ID33=\t"+str(oth.getBoilerReg(33))+"\texhoust temperature")
#	time.sleep(0.1)
	#print("Boiler ID116=\t"+str(oth.getBoilerReg(116))+"\tburner starts")
	#time.sleep(0.5)
	print("Boiler ID17=\t"+str(oth.getBoilerReg(17)/256.0)+"\t Relative Modulation Level")
#	time.sleep(0.1)
	print("Boiler ID25=\t"+str(oth.getBoilerReg(25)/256.0)+"\t Boiler water temp")
#	time.sleep(0.1)
	print("Boiler ID26=\t"+str(oth.getBoilerReg(26)/256.0)+"\t DHW temperature")
#	time.sleep(0.1)
	print("Boiler ID28=\t"+str(oth.getBoilerReg(28)/256.0)+"\t Return water temperature")
#	time.sleep(0.1)
	print("Boiler ID116=\t"+str(oth.getBoilerReg(116))+"\t burner starts")

