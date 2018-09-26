# coding=utf-8
import requests
import logging as log

SERVER_ADDRESS = 'http://localhost:8080'
REGISTER_DEVICE_URL = '/v1/devices/register'
UPDATE_STATUS_URL = '/v1/devices/update/state'
GET_TARGET_TEMP_IRL = '/v1/devices/temp/target'
PING_URL = '/v1/ping'

API_TOKEN_FILE = "api_token"


class DeviceStatus:
    def __init__(self):
        pass

    WORKING = "WORKING"
    REBOOT = "REBOOT"


class API:

    def __init__(self):
        try:
            self.__api_token = self.__read_token()
        except IOError as e:
            log.error("Can't read api token file. %s" % e)
            self.__api_token = ""

    def update_state(self, balance, current_temp, status):
        response = requests.put(SERVER_ADDRESS + UPDATE_STATUS_URL,
                                json={
                                    "balance": balance,
                                    "current_temp": {
                                        "value": current_temp,
                                        "scale": "CELSIUS"
                                    },
                                    "device_status": status
                                },
                                headers={"deviceAuthToken": self.__api_token})
        if response.status_code != 200:
            log.error("Error while updating device status. "
                      "HTTP status code: %s; "
                      "response: '%s'"
                      % (response.status_code, response.content))

    def get_target_state(self):
        response = requests.get(SERVER_ADDRESS + GET_TARGET_TEMP_IRL,
                                headers={"deviceAuthToken": self.__api_token})
        if response.status_code != 200:
            log.error("Error while loading current target temp. "
                      "HTTP status code: %s; "
                      "response: '%s'"
                      % (response.status_code, response.content))

        return response.json()["result"]

    def is_authorized(self):
        return bool(self.__api_token)

    def register_device(self, serialNumber):
        response = requests.post(SERVER_ADDRESS + REGISTER_DEVICE_URL,
                                 json={
                                     "token": self.__api_token,
                                     "serial_number": serialNumber
                                 },
                                 headers={
                                     "Content-Type": "application/json"
                                 })
        if response.status_code != 200:
            log.error("Device registration failed. "
                      "HTTP status code: %s; "
                      "response: '%s'"
                      % (response.status_code, response.content))
            return False
        log.info("Device is registered successfully")
        return True

    @staticmethod
    def save_token(token):
        token_file = open(API_TOKEN_FILE, "w")
        token_file.write(token)
        token_file.close()

    @staticmethod
    def __read_token():
        token_file = open(API_TOKEN_FILE, "r")
        return token_file.read()
