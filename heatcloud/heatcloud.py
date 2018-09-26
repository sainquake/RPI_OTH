#!/usr/bin/python
# coding=utf-8
from __future__ import print_function

from time import sleep

import logging as log
import sys
import os

import driver
from api import API
from api import DeviceStatus
from daemon import Daemon

MAIN_LOOP_DELAY = 5
PID_FILE = "heatcloud.pid"
log.basicConfig(filename="heatcloud.log",
                level=log.DEBUG,
                format="%(filename)s:%(lineno)d# \t%(levelname) \t[%(asctime)s] \t%(message)s")
log.getLogger().addHandler(log.StreamHandler())


class Main(Daemon):

    def __init__(self, pidfile, stdin=os.devnull,
                 stdout=os.devnull, stderr=os.devnull,
                 home_dir='.', umask=0o22, verbose=1,
                 use_gevent=False, use_eventlet=False):
        super(Main, self).__init__(pidfile, stdin=os.devnull, stdout=os.devnull, stderr=os.devnull, home_dir='.',
                                   umask=0o22, verbose=1, use_gevent=False, use_eventlet=False)

        self.api_instance = API()

    def start(self, *args, **kwargs):
        if not self.api_instance.is_authorized():
            log.error("Device is not registered on server(file with api token not exists or empty)")
            exit(1)
        super(Main, self).start(*args, **kwargs)

    def run(self):
        while True:
            try:
                target_state = self.api_instance.get_target_state()
                if target_state["need_reboot"]:
                    current_temp = driver.get_current_temp()
                    balance = driver.get_sim_balance()
                    self.api_instance.update_state(balance, current_temp, DeviceStatus.REBOOT)
                    driver.reboot()
                else:
                    driver.set_target_temp(target_state["target_temp"])
                    current_temp = driver.get_current_temp()
                    balance = driver.get_sim_balance()
                    self.api_instance.update_state(balance, current_temp, DeviceStatus.WORKING)

                sleep(MAIN_LOOP_DELAY)
            except Exception as e:
                log.error(e)
                sleep(MAIN_LOOP_DELAY)


def get_device_name():
    try:
        return open("device_serial_number.txt").readline()
    except IOError:
        return "test device"


def authenticate(token):
    log.info("authentication...")
    API.save_token(token)
    api_instance = API()
    return api_instance.register_device(get_device_name())


if len(sys.argv) != 2:
    if len(sys.argv) == 3 and sys.argv[1] == "sms":
        if authenticate(sys.argv[2]):
            Main(PID_FILE).start()
        else:
            log.error("Device was not registered. Exit...")
            exit(1)
    else:
        log.error("invalid args count")
        exit(1)
elif sys.argv[1] == "start":
    Main(PID_FILE).start()
elif sys.argv[1] == "stop":
    Main(PID_FILE).stop()
elif sys.argv[1] == "restart":
    Main(PID_FILE).restart()
else:
    log.error("invalid command %s" % sys.argv[1])
    exit(1)
