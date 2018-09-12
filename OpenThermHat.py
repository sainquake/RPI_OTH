# -*- coding: utf-8 -*-
#!/usr/bin/env python

import serial
import RPi.GPIO as GPIO
import time

class OpenThermHat:
    def __init__(self):
        print "init"
        # Use "logical" pin numbers
        GPIO.setmode(GPIO.BCM)
        # Disable "This channel is already in use" warnings
        GPIO.setwarnings(False)

        # Setup MCU POWER UP
        GPIO.setup(17, GPIO.OUT)
        GPIO.output(17, True)
        #LEDS
        GPIO.setup(4, GPIO.OUT)
        GPIO.output(4, True)

        GPIO.setup(27, GPIO.OUT)
        GPIO.output(27, True)

        GPIO.setup(6, GPIO.OUT)
        GPIO.output(6, True)

        self.ser = serial.Serial ("/dev/ttyAMA0")    #Open named port
        self.ser.baudrate = 115200                     #Set baud rate to 9600
        self.ser.timeout = 1
    def sendReceive(ad0,ad1,data0,data1)
        # address0 address1 data0 data1
        values = bytearray([ad0, ad1, data0, data1])
        ser.write(values)
        time.sleep(0.1)
        data = ser.read(4)
        print 'data=' , ":".join("{:02x}".format(ord(c)) for c in data)
        return data
