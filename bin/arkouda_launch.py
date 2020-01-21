#!/usr/bin/python3
# coding=utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

import os,sys
import time
import json
import arkouda as ak 
arkouda_server= '10.50.150.98'
arkouda_port = '5555'
data_set = 'inital_range'
data_type= 'array'
search_string='500493'
ak_server = arkouda_server
ak_port = arkouda_port
data_set = data_set
data_type = data_type
search_string = search_string
ak.connect(ak_server,ak_port)
dropped = sys.stdout
error = sys.stderr 
sys.stdout = open('temp.txt','w')
sys.stdout = dropped 
sys.stderr = open('temp.txt', 'w')
sys.stderr = error
search=ak.load(data_set, dataset=data_type)
print(search_string)
print(search)
print(ak.min(search))
