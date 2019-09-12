# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 14:06:12 2018

@author: tobeywang
"""
import json
import logging
import getpass
jsonfile='personinfo.json'
user_id=input("Enter your id:")
pswd = getpass.getpass('Password:')
value= {'id' : user_id, 'pw' : pswd }
try:
    with open(jsonfile, 'w+') as fp:
        json.dump(value, fp)
        fp.close()
except Exception as error:
    logging.getLogger('').handlers = []

    logging.basicConfig(filename = "plog.log",
    filemode="w",
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')