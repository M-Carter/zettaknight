#!/usr/bin/python

from zk_utils import spawn_job
import logging

logger = logging.getLogger(__name__)
    
    
def get_live_datasets():
    '''query zfs to return a tuple of all datasets'''
    
    datasets_list = []
    logger.debug('running zfs list -H')
    datasets = spawn_job('zfs list -H')
    logger.debug(datasets)
    
    logger.debug('formatting output...')
    for line in datasets.split('\n'):
        logger.debug('line is {0}'.format(line))
        line = line.split()
        if line:
            dataset = line[0]
            logger.debug('adding dataset {0}'.format(dataset))
            datasets_list.append(dataset)
        
    #convert list to tuple
    logger.info('live datasets: {0}'.format(datasets_list))
    return datasets_list
    

def get_dataset_attributes(dataset, attributes=None):
    '''
    for a given dataset, return attributes given in list format.  If attributes
    is empty, return all attributes
    '''
    
    assert dataset is not None, 'a dataset must be given'
    
    if attributes:
        assert isinstance(attributes, list), 'attributes must be a list'
        
    ret = {}
        
    dataset_attributes = spawn_job('zfs get all {0} -H'.format(dataset))
    logger.debug('dataset {0} attributes: {1}'.format(dataset, dataset_attributes))
    
    for line in dataset_attributes.split('\n'):
        logger.debug('line is {0}'.format(line))
        line = line.split()
        if line:
            name_ = line[0]
            key_ = line[1]
            value_ = line[2]
            
            logger.debug('name:{0}, key:{1}, value:{2}\n'.format(name_, key_, value_))

            if name_ not in ret:
                logger.debug('{0} not in ret, creating'.format(name_))
                ret[name_] = {}
                    
            if attributes:
                if key_ in attributes:
                    ret[name_] = value_
                else:
                    logger.debug('key {0} not in attributes, ignoring...'.format(key_))
            else:
                ret[name_] = value_
    
    logger.info('ret: {0}'.format(ret))
    return ret
        
def get_all_live_datasets():
        '''function runs a zfs get all and returns a string output'''
        ret = {}
        logger.debug('getting zfs list information')
        datasets = spawn_job('zfs list -H')
        logger.debug(datasets)
        for line in datasets.split('\n'):
            logger.debug(line)
            dataset = line.split()[0]
            logger.debug(dataset)
            dataset_config = spawn_job('zfs get all {0} -H'.format(dataset))
            for line in dataset_config.split('\n'):
                logger.debug(line)
                
                line = line.split()
                name_ = line[0]
                key_ = line[1]
                value_ = line[2]
                
                #create the key if it doesn't exist
                if name_ not in ret:
                    ret[name_] = {}

                ret[name_][key_] = value_
                    
        return ret
        
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