'''
Created on 13.09.2011

@author: corwin
'''

global DEBUG
DEBUG = True

PORT = 8080
SERVER = '127.0.0.1'

JSON_DUMPS_FORMAT = {
    "sort_keys": "true",
    "indent": 4,
}

DB_CONFIG = {
    "location": "./db",
    "user": "",
    "password" : ""
}

USERNAME_MIN_LEN = 3
USERNAME_MAX_LEN = 16

PASSWORD_MIN_LEN = 6
PASSWORD_MAX_LEN = 18

usrnameRegexp = r'^[a-z]+[\w_-]{%s,%s}$' % (USERNAME_MIN_LEN- 1, USERNAME_MAX_LEN - 1)
pasRegexp = r'^.{%s,%s}$' % (PASSWORD_MIN_LEN, PASSWORD_MAX_LEN)
