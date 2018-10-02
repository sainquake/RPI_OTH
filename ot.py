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
	print("Boiler ID3=\t"+str(oth.getBoilerID()) + "\t boiler id")
	time.sleep(0.5)
	print("Boiler ID0=\t"+str(oth.getBoilerReg(0)) + "\t status")
	time.sleep(0.5)
	print("Boiler ID5=\t"+str(oth.getBoilerReg(5)) + "\tflags")
	time.sleep(0.5)
	print("Boiler ID28=\t"+str(oth.getBoilerReg(28)/256.0)+"\tReturn water temperature")
	time.sleep(0.5)
	print("Boiler ID33=\t"+str(oth.getBoilerReg(33))+"\texhoust temperature")
	time.sleep(0.5)
	print("Boiler ID116=\t"+str(oth.getBoilerReg(116))+"\tburner starts")
	time.sleep(0.5)
	print("Boiler ID17=\t"+str(oth.getBoilerReg(17)/256.0)+"\t Relative Modulation Level")
	time.sleep(0.5)
	print("Boiler ID25=\t"+str(oth.getBoilerReg(25)/256.0)+"\t Boiler water temp")
	time.sleep(0.5)
	print("Boiler ID26=\t"+str(oth.getBoilerReg(26)/256.0)+"\t DHW temperature")
	time.sleep(0.5)
	print("Boiler ID28=\t"+str(oth.getBoilerReg(28)/256.0)+"\t Return water temperature")