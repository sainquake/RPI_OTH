#!/usr/bin/env python3
from OpenThermHat import GSM

gsm = GSM()

try:
	if not gsm.isEnabled():
		print("need to reset")
		print("GSM not working;terminate")
	else:
		print("module enabled "+str(True))
	
	print("fun:"+str(gsm.getFun()) )
	print("getCPIN:"+str(gsm.getCPIN()) )
	print("last sms:"+str(gsm.readLastSMS()) )
	print(gsm.getUnicNumber() )
	print("charge "+str(gsm.getBatteryCharge())+"%" )
	print("charge "+str(gsm.getBatteryVoltage())+"V" )
	print("signal quality "+ str(gsm.getSignalQuality())+"/31")
	
	print("operator "+gsm.getOperator())
	#gsm.deleteAllSMS()
	
	
	
except KeyboardInterrupt:
	print( '! ^C received, shutting down')
	gsm.close()