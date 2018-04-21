#!/usr/bin/python

import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1953000

# Split an integer input into a two byte array to send via SPI
def write_pot(input):
	hsb = input >> 16 & 0xFF
	msb = input >> 8 & 0xFF
	lsb = input & 0xFF
	spi.xfer([hsb, msb, lsb])

# Repeatedly switch a MCP4151 digital pot off then on
while True:
	write_pot(0x010203)
	time.sleep(0.5)
