#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from OpenThermHat import OpenThermHat
import time

oth = OpenThermHat()
while True:
	oth.sendReceive(OpenThermHat.RPi_ECHO_UART_ADDRESS,0,0,4)
	time.sleep(0.5)
	oth.setTemp(52)
	time.sleep(0.5)	
	print("indorTemp=\t"+str(oth.getTemp()))
	time.sleep(0.5)	
	print ("USB Voltage=\t"+str(oth.getADC(6)))
	time.sleep(0.5)
	print("BoilerID=\t"+str(oth.getBoilerID()))
	time.sleep(0.5)
	print("BoilerSwitchedOff=\t"+str(oth.getOpenTermStatus(0)))
	time.sleep(0.5)
	print("hardware id=\t"+str(oth.getMem(0)))
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

