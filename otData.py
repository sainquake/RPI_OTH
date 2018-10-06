#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from OpenThermHat import OpenThermHat
import time

oth = OpenThermHat()
oth.resetMCU()
while True:
	echo = oth.sendReceive(OpenThermHat.RPi_ECHO_UART_ADDRESS,0,4,5)
	#if echo[]
	if (echo>>16)&0xFFFF!=0x0504:
		oth.resetMCU()
		print("RESET MCU")

	time.sleep(5)
	
	otStatus = oth.getOpenTermStatus(6)
	print("#otStatus=\t"+str(otStatus))
	boilerStatus = oth.getBoilerReg(0)
	print("#boilerStatus=\t"+str(boilerStatus))
	boilerConfig = oth.getBoilerReg(3)
	print("#boilerConfig=\t"+str(boilerConfig))
	errorFlags = oth.getBoilerReg(5)
	print("#errorFlags=\t"+str(errorFlags))
		
	oth.getOTStatus()
	print("#otStatus=\t"+str(oth.otStatus))
	print("ot.timeout=\t"+str(oth.otData.otTimeout))
	print("ot.index=\t"+str(oth.otData.otIndex))
	print("ot.busy=\t"+str(oth.otData.otBusy))
	print("ot.complete=\t"+str(oth.otData.otComplete))
	print("ot.frameSendedAndStartWaitingACK=\t"+str(oth.otData.otFrameSendedAndStartWaitingACK))
	print("ot.readingResponse=\t"+str(oth.otData.otReadingResponse))
	print("ot.specialRequest=\t"+str(oth.otData.otSpecialRequest))
	print("ot.specialRequestComplete=\t"+str(oth.otData.otSpecialRequestComplete))
	
	print("#boilerStatus=\t"+str(oth.boilerStatus))
	print("boilerFault=\t"+str(oth.otData.boilerFault))
	print("boilerCHMode=\t"+str(oth.otData.boilerCHMode))
	print("boilerDHWMode=\t"+str(oth.otData.boilerDHWMode))
	print("boilerFlameStatus=\t"+str(oth.otData.boilerFlameStatus))
	print("boilerCoolingStatus=\t"+str(oth.otData.boilerCoolingStatus))
	print("boilerCH2Mode=\t"+str(oth.otData.boilerCH2Mode))
	print("boilerDiagnostic=\t"+str(oth.otData.boilerDiagnostic))
	
	print("#boilerConfig=\t"+str(oth.boilerConfig))
	print("boilerMemberID=\t"+str(oth.otData.boilerMemberID))
	print("boilerDHWPresent=\t"+str(oth.otData.boilerDHWPresent))
	print("boilerControlType=\t"+str(oth.otData.boilerControlType))
	print("boilerCoolingConfig=\t"+str(oth.otData.boilerCoolingConfig))
	print("boilerDHWConfig=\t"+str(oth.otData.boilerDHWConfig))
	print("boilerPumpControlFunction=\t"+str(oth.otData.boilerPumpControlFunction))
	print("boilerCH2Present=\t"+str(oth.otData.boilerCH2Present))
	
	print("#errorFlags=\t"+str(oth.errorFlags))
	print("errorOEM=\t"+str(oth.otData.errorOEM))
	print("errorServiceRequered=\t"+str(oth.otData.errorServiceRequered))
	print("errorLockoutReset=\t"+str(oth.otData.errorLockoutReset))
	print("errorLowWaterPress=\t"+str(oth.otData.errorLowWaterPress))
	print("errorGasFlameFault=\t"+str(oth.otData.errorGasFlameFault))
	print("errorAirPressureFault=\t"+str(oth.otData.errorAirPressureFault))
	print("errorWaterOverTemperature=\t"+str(oth.otData.errorWaterOverTemperature))
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
	print("Boiler ID19=\t"+str(oth.getBoilerReg(19))+"\t l/min flow")
	#requests with waiting for response
	print("set temp"+ str(oth.setTemp(55)))
#	print("Boiler ID1=\t"+str(oth.getBoilerReg((1<<7) +1,44*256)/256.0)+"\t set water temp")
	while not( (oth.getOpenTermStatus(6)>>6)&1 ):
		time.sleep(0.5)
	print("set temp"+ str(oth.setTemp(55)))
#	print("Boiler ID1=\t"+str(oth.getBoilerReg((1<<7) +1,44*256)/256.0)+"\t set water temp")
	
#	print("Boiler ID8=\t"+str(oth.getBoilerReg((1<<7) +8,33*256)/256.0)+"\t Control setpoint 2")
#	while not( (oth.getOpenTermStatus(6)>>6)&1 ):
#                time.sleep(0.5)
#	print("Boiler ID8=\t"+str(oth.getBoilerReg((1<<7) +8,33*256)/256.0)+"\t Control setpoint 2")
	
#	print("Boiler ID16=\t"+str(oth.getBoilerReg((1<<7) +16,22*256)/256.0)+"\t Room setpoint")
#	while not( (oth.getOpenTermStatus(6)>>6)&1 ):
#		time.sleep(0.5)
#	print("Boiler ID16=\t"+str(oth.getBoilerReg((1<<7) +16,22*256)/256.0)+"\t Room setpoint")
