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
	boilerSwitchedOff = oth.getOpenTermStatus(0)
	print("BoilerSwitchedOff=\t"+str(boilerSwitchedOff))
	time.sleep(0.5)
	print("Boiler ID3=\t"+str(oth.getBoilerID()))
	time.sleep(0.5)
	print("Boiler ID0=\t"+str(oth.getBoilerReg(0)))
	time.sleep(0.5)
	print("Boiler ID5=\t"+str(oth.getBoilerReg(5)))
