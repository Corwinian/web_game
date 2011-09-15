#!/usr/bin/python
'''
Created on 11.09.2011

@author: corwin
'''

import json
import errors
import db_commect

actions = dict(
               "register"= "register_user",
               "login"= "login_user",
               "logout"= "logout_user",
               )


def parse_request(json):
    try
        json = json.loads(json)
        
        if not isinstance(json, dict):
            raise BadRequest("Json must be is object")
        try:
            comand  = json["cmd"]
            try:
                return actions[comand](json)
            except (KeyError):
                raise BadCommand("UnIndefined command")
            except (RequestException) e:
                raise e
        except (KeyError):
            raise BadRequest("not commands")
        
    except (TypeError):
        raise BadRequest("Request is not json")
    
def register_user(json):
    try #gпотом могет из дб кидать
        user = User(json)
        
    except (KeyError):
            raise BadCommand("badparams")   
    return

def login_user(json):
    return

def logout_user(json):
    return
    
    