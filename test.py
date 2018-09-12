#!/usr/bin/env python
# -*- coding: utf-8 -*-
import OpenThermHat
import time

oth = OpenThermHat()

while True:
    oth.sendReceive(1,1,1,1)
    time.sleep(0.5)
