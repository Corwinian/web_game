#!/usr/bin/python
'''
Created on 11.09.2011

@author: corwin
'''

import json
import errors
import db_connect

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
            comand  = json.pop("cmd")
            try:
                return actions[comand](**json)
            except (KeyError):
                raise BadCommand("UnIndefined command")
            except (TypeError):
                raise BadCommand("bad command")
            except (RequestException) e:
                raise e
        except (KeyError):
            raise BadRequest("not commands")
        
    except (TypeError):
        raise BadRequest("Request is not json")
    
def register_user(user, password):
    try #gпотом могет из дб кидать
        user = User(user, password)
        userInDb = data_Base.query(User).filter_by(name = user.name).one()
        if ()
    except sqlalchemy.orm.exc.NoResultFound:
        user = User(username, password)
        dbi().add(user)
    except (KeyError):
        raise BadCommand("bad params")   
    return

def login_user(json):
    return

def logout_user(json):
    return
    
    