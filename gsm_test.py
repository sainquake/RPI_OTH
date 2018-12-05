#!/usr/bin/env python3
from OpenThermHat import GSM

gsm = GSM()

try:
	if not gsm.isEnabled():
		print("need to reset")
		print("GSM not working;terminate")
		quit()
	else:
		print("module enabled "+str(True))
	if not gsm.isSIMInserted():
		print("sim is not inserted; reset")
		gsm.softwareReset()
		if not gsm.isSIMInserted():
			print("sim is not inserted; terminate")
			quit()
	#print("reset:"+str(gsm.softwareReset()) )
	print("fun:"+str(gsm.getPhoneFunctionality()) )
	
	print("isSIMInserted:"+str(gsm.isSIMInserted()) )
	print("getCOPS:"+str(gsm.getCOPS()) )
	print("getPhoneActivityStatus:"+str(gsm.getPhoneActivityStatus()) )
	
	
	print("last sms:"+str(gsm.readLastSMS()) )
	print(gsm.getUnicNumber() )
	print("charge "+str(gsm.getBatteryCharge())+"%" )
	print("charge "+str(gsm.getBatteryVoltage())+"V" )
	print("signal quality "+ str(gsm.getSignalQuality())+"/31")
	
	print("operator "+gsm.getOperator())
	#gsm.deleteAllSMS()
	quit()
	
	
except KeyboardInterrupt:
	print( '! ^C received, shutting down')
	gsm.close()