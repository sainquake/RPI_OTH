#!/usr/bin/env python3
from OpenThermHat import GSM

gsm = GSM()

try:
	if not gsm.isEnabled():
		print("need to reset")
		print("GSM not working;terminate")
		break
	else:
		print("module enabled "+str(True))
	
	print("last sms:"+gsm.readLastSMS() )
	print(gsm.getUnicNumber() )
	print("charge "+str(gsm.getBatteryCharge())+"%" )
	
	print("signal quality"+ str(gsm.getSignalQuality()))
	
	print("operator "+gsm.getOperator())
	#gsm.deleteAllSMS()
	
	
	
except KeyboardInterrupt:
	print( '! ^C received, shutting down')
	gsm.close()