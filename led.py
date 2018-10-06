#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from OpenThermHat import OpenThermHat
import time

oth = OpenThermHat()
oth.resetMCU()

#print("fff"+str(None))
while True:
	echo = oth.sendReceive(OpenThermHat.RPi_ECHO_UART_ADDRESS,0,4,5)
	#if echo[]
	if (echo>>16)&0xFFFF!=0x0504:
		oth.resetMCU()
		print("RESET MCU")
		oth.ledControl(oth.RED,False)
	else:
		oth.ledControl(oth.RED,True)

	gsmModuleOff = oth.getGSM(0)
	oth.ledControl(oth.BLUE,not gsmModuleOff)
	print("GSM module off\t"+str(gsmModuleOff))
	
	oth.getOTStatus()
	print("boiler module off\t"+str(oth.otData.otTimeout))
	oth.ledControl(oth.GREEN,not oth.otData.otTimeout)
	
	time.sleep(1)

