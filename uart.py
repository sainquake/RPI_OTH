#!/usr/bin/python

import serial
import time

uart = serial.Serial("/dev/ttyAMA0")
uart.boudrate = 115200

# Split an integer input into a two byte array to send via SPI
def write_pot(input):
	hsb = input >> 16 & 0xFF
	msb = input >> 8 & 0xFF
	lsb = input & 0xFF
	uart.write("Hel")

# Repeatedly switch a MCP4151 digital pot off then on
while True:
	write_pot(0x010203)
	time.sleep(0.5)
