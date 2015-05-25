# -*- coding: utf-8 -*-
import hashlib
import jwt
import json
import random
import string
from base64 import b64encode, b64decode
from datetime import datetime

PADDING = r'%'

def hash_passwd(passwd, salt):
    return hashlib.sha512(salt.encode() + passwd.encode()).hexdigest()

def generate_token(json_dict, secret, algo):
    token = jwt.encode(json_dict, secret, algo)
    return token

def decrypt_token(token, secret, algo):
    json_dict = jwt.decode(token, secret, algo)
    return json_dict

def get_user_from_token(token, secret, algo):
    json_dict = decrypt_token(token, secret, algo)
    user = json_dict['user']
    expired_time = datetime.strptime(json_dict['expired'], '%Y-%m-%d %H:%M:%S')

    try:
        reset = json_dict['reset']
    except:
        reset = 0

    if datetime.now() > expired_time:
        raise Exception('token expired')

    if reset == 1:
        raise Exception('not login token')

    return user

def get_user_from_reset_passwd(token, secret, algo):
    json_dict = decrypt_token(token, secret, algo)
    user = json_dict['id']
    print json_dict
    expired_time = datetime.strptime(json_dict['expired'], '%Y-%m-%d %H:%M:%S')

    try:
        reset = json_dict['reset']
    except:
        reset = 0

    if datetime.now() > expired_time:
        raise Exception('token expired')

    if reset != 1:
        raise Exception('not reset password token')

    return user


def is_correct_passwd(db_passwd, passwd, salt):
    return db_passwd == hash_passwd(passwd, salt)
    
