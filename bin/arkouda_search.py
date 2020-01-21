#!/usr/bin/python3
# coding=utf-8

#from subprocess import call
#call('python3 arkouda_launch.py', shell=True)

from __future__ import absolute_import, division, print_function, unicode_literals
import os,sys
import time
import json
import arkouda as ak 
#arkouda_server= '10.50.150.98'
#arkouda_port = '5555'
#data_set = 'inital_range'
#data_type= 'array'
#search_string='500493'

#ak.connect(arkouda_server, arkouda_port)

splunkhome = os.environ['SPLUNK_HOME']
sys.path.append(os.path.join(splunkhome, 'etc', 'apps', 'searchcommands_app', 'lib'))
from splunklib.searchcommands import dispatch, StreamingCommand, Configuration, Option, validators
from splunklib.six.moves import range

@Configuration()
class ArkoudaSearch(StreamingCommand):
    """ Sends Search Request to Arkouda.
    This is the inital proto-type, additional testing is required and additional commands can be addded.
    ##Syntax
    .. code-block::
        arkoudasearch arkouda_server=<server ip or fqdn> arkouda_port=<port number> data_set=<data set to search> data_type=<type of data being searched array etc> search_string=<search to run in arkouda> 
    ##Description
    arkoudasearch dispatchs a search to the arkouda server defined in the search, then returns results to Splunk for further data evaluation
    ##Example
    Dispatch search to arkouda and return results 
    .. code-block::
        index=firewall src=2.3.4.1 | arkoudasearch arkouda_server='10.50.150.98' arkouda_port='5555' data_set='inital_range' data_type='array' search_string='2.3.4.1'
    """
    arkouda_server = Option(
        doc='''
        **Syntax:** **arkouda_server=***<arkouda_server>*
        **Description:** Name of the Arkouda Server''')

    arkouda_port = Option(
        doc='''
        **Syntax:** **arkouda_port=***<port_number>*
        **Description:**Port Number of Arkouda Server''')

    data_set = Option(
        doc='''
        **Syntax:** **data_set=***<name of data set to load and search>*
        **Description:** Specifies the data set to Load and search.''')

    data_type = Option(
        doc='''
        **Syntax:** **data_type=***<type of data being searched>*
        **Description:** Specifies the data type that is being searched.''')

    search_string = Option(
        doc='''
        **Syntax:** **search_string=***<What is being searched for>*
        **Description:** Specifies the string / value to search in arkouda for ''')


    def stream(self, records):
        self.logger.debug('Arkouda_Search_Command: %s', self)  # logs command line
        ak_server = self.arkouda_server
        ak_port = self.arkouda_port
        data_set = self.data_set
        data_type = self.data_type
        search_string = self.search_string
        ak.connect(ak_server,ak_port)
        search=ak.load(data_set, dataset=data_type)
        for record in records:
         result = ak.min(search)
         record['Search_results'] = result
         yield record
dispatch(ArkoudaSearch, sys.argv, sys.stdin, sys.stdout, __name__)

