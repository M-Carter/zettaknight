#!/usr/bin/python

import six
import logging
import sys

from zk_import import ZkZpools
from zk_import import ZkZettaknight

logging.basicConfig(level=logging.DEBUG)
#logger = logging.getLogger()
#my_format = logging.Formatter('%(asctime)s %(module)-12s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p')
#handler = logging.StreamHandler(sys.stdout)
#handler.setFormatter(my_format)
#logger.addHandler(handler)

logging.info('Zettaknight Dev is starting...')



zpool_conf_file = '/etc/zettaknight/len010.clemson.edu_zpool.conf'
zettaknight_conf_file = '/etc/zettaknight/zettaknight.conf'
 
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
        