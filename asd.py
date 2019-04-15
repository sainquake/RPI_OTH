#!/usr/bin/env python3

from OpenThermHat import OpenThermHat
import time


oth = OpenThermHat()
print("set temp...")
print(oth.setTemp(52))
print("get temp...")
print(oth.getTemp())
