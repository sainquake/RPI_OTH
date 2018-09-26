import logging as log


def get_current_temp():
    log.info("get temp")
    return 36.6


def get_sim_balance():
    log.info("get balance")
    return 100


def reboot():
    log.info("reboot....")


def set_target_temp(temp):
    log.info("set temp; %s" % temp)
