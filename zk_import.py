#!/usr/bin/python

import yaml
import json
import six
import logging

from zk_utils import spawn_job

#open logging instance
logger = logging.getLogger(__name__)

class ZkBase(object):
    def __init__(self):        
        pass
        
    def conv_str_to_dict(self, string):
    
        '''
        takes a console output and breaks each line on a newline, then
        creates a formatted dictionary out of the first three columns
        
        ouput_dict['column1']['column2'] = 'column3'
        '''

        logger.debug('converting string input to a usable dictionary...')
        assert isinstance(string, str) and string is not None, 'conv_str_to_dict requires a string'
        
        ret = {}
        
        for line in string.split('\n'):
            #create a list from string
            line = line.split()

            if line:
                name_ = line[0]
                key_ = line[1]
                value_ = line[2]

                #create the key if it doesn't exist
                if name_ not in ret:
                    ret[name_] = {}

                ret[name_][key_] = value_
        
        return ret
        
        
class ZkDatasets(ZkBase):
    def __init__(self):
        self.live_datasets = None
        self.defined_datasets = None
        
    def get_all_live_datasets(self):
        '''function runs a zfs get all and returns a string output'''
        
        dataset_configs = spawn_job('zfs get all -H')
        return dataset_configs
        
    def live_datasets(self):
    
        '''
        takes the output from get_all_live_datasets and creates a usable dictionary
        format will be dictionary['dataset']['zfs attribute'] = value
        '''
        
        dataset_configs = self.get_all_live_datasets()
        return super(ZkDatasets, self).conv_str_to_dict(dataset_configs)
        
        
class ZkZpools(ZkBase):
    def __init__(self):
        self.live_zpools = None
        self.defined_zpools = None
        
    def get_all_live_zpools(self):
    
        '''function runs a zpool get all and returns a string output'''

        logger.debug('generating zpool get all statement...')
        zpool_configs =  spawn_job('zpool get all -H')
        return zpool_configs
        
    def get_live_zpools(self):
    
        '''
        takes the output from get_all_live_zpools and creates a usable dictionary
        format will be dictionary['pool name']['zfs attribute'] = value
        '''

        logger.debug('retrieving live zpool information...')
        zpool_configs = self.get_all_live_zpools()
        zpool_dict = super(ZkZpools, self).conv_str_to_dict(zpool_configs)
        return zpool_dict
        
    def get_defined_zpools(self, file):
        
        '''open the zettaknight zpool configuration file and converts to a usable dictionary'''
        
        logger.debug('retrieving zettaknight zpools from {0}...'.format(file))
        assert file is not None

        with open(file, 'r') as f:
            conff = yaml.safe_load(f)
            
        return conff
        

class ZkZettaknight:
    def __init__(self):
        pass
        
    def get_zettaknight_config(self, file):
        '''open the zettaknight configuration file and converts to a usable dictionary'''
        
        logger.debug('retrieving zettaknight configuration from {0}...'.format(file))
        assert file is not None

        with open(file, 'r') as f:
            conff = yaml.safe_load(f)
            
        return conff
    
