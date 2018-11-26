#!/usr/bin/env python3
from OpenThermHat import GSM

gsm = GSM()

try:
	req = gsm.sendReceive("AT\r\n")
	print("module enabled "+str(gsm.OK))
	
	print("last sms:"+gsm.readLastSMS() )
	print(gsm.getUnicNumber() )
	print("charge "+str(gsm.getBatteryCharge())+"%" )
	
	print("signal quality"+ str(gsm.getSignalQuality()))
	
	#gsm.deleteAllSMS()
	
except KeyboardInterrupt:
	print( '! ^C received, shutting down')
	gsm.close()