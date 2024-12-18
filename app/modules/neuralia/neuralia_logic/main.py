# -*-coding: utf-8 -*-

import configparser
 
config = configparser.ConfigParser()
config.read('../../../../etc/config.ini')

api_key = config['DEFAULT']['Api_key']
print(api_key)
