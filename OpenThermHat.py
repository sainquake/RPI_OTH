# -*- coding: utf-8 -*-
#!/usr/bin/env python

import serial
import RPi.GPIO as GPIO
import time

class OpenThermHat:
    ser
    def init():
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

        ser = serial.Serial ("/dev/ttyAMA0")    #Open named port
        ser.baudrate = 115200                     #Set baud rate to 9600
        ser.timeout = 1
    def
