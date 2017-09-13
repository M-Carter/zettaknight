#!/usr/bin/python

import six
import logging
import sys

from zk_import import ZkZpools
from zk_import import ZkZettaknight
from zk_import import ZkDatasets
from zk_utils2 import get_live_datasets
from zk_utils2 import get_dataset_attributes

logging.basicConfig(level=logging.DEBUG)
#logger = logging.getLogger()
#my_format = logging.Formatter('%(asctime)s %(module)-12s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p')
#handler = logging.StreamHandler(sys.stdout)
#handler.setFormatter(my_format)
#logger.addHandler(handler)

logging.info('Zettaknight Dev is starting...')

zettaknight_conf_file = '/etc/zettaknight/zettaknight.conf'


#-----------------------------------------------------------------------
#find zpool information
#-----------------------------------------------------------------------

zpool_conf_file = '/etc/zettaknight/len010.clemson.edu_zpool.conf'

try:
    zkpools = ZkZpools()
    live_zpools = zkpools.get_live_zpools()
    deployed_zpools = zkpools.get_defined_zpools(zpool_conf_file)
    
    zkzettaknight = ZkZettaknight()
    zettaknight_config = zkzettaknight.get_zettaknight_config(zettaknight_conf_file)
    
except Exception as e:
    logging.error(e)
    sys.exit(1)


for zpool, zpool_config in six.iteritems(live_zpools):
    for key, value in six.iteritems(zpool_config):
        print key, value
    
for zpool, zpool_config in six.iteritems(deployed_zpools):
    for key, value in six.iteritems(zpool_config):
        print key, value

#-----------------------------------------------------------------------
#find dataset information
#-----------------------------------------------------------------------

live_datasets = get_live_datasets()
print live_datasets

for dataset in live_datasets:
    attr = get_dataset_attributes(dataset)
    sys.exit(0)

#-----------------------------------------------------------------------
        