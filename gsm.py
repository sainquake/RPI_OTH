#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from OpenThermHat import OpenThermHat
import time

oth = OpenThermHat()
oth.resetMCU()
echo = oth.sendReceive(OpenThermHat.RPi_ECHO_UART_ADDRESS,0,4,5)
if (echo>>16)&0xFFFF!=0x0504:
	oth.resetMCU()
	print("RESET MCU")
while True:	
	gsmModuleOff = oth.getGSM(255)
	print("GSM module off\t"+str(gsmModuleOff))
	print("GSM module (AT) enabled=\t"+str(oth.getGSM(0)))
	print("GSM module (AT+CSQ) network quality (>10 is good)=\t"+str(oth.getGSM(21)))
	print("GSM module (AT+CPIN) SIM inserted=\t"+str(oth.getGSM(9)))
	print("GSM module (AT+CBC) battery voltage(mV)=\t"+str(oth.getGSM(23)))
	print("GSM smsCount:"+str(oth.getGSM(25)))
	#print("GSM operator:"+str(oth.getOperator()))
	print("\n\n=======================\n\n")
	time.sleep(10)