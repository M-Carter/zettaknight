#!/usr/bin/python

def dummy_function():
    print 'I gotz here!'

def create_environment():

    if not os.path.isfile(zettaknight_globs.config_file_new):
        shutil.copy(zettaknight_globs.default_config_file, zettaknight_globs.config_file_new)
                    
    if not os.path.isfile(zettaknight_globs.pool_config_file):
        shutil.copy(zettaknight_globs.default_pool_config_file, zettaknight_globs.pool_config_file)
        
    set_global_vars()
    
    
    

#        out0 = build_out_config()
#       out1 = create_crond_file()
#        out2 = backup_luks_headers()
#       out3 = backup_files()
#      if not os.path.isfile(zettaknight_globs.identity_file):
#         ssh_keygen(zettaknight_globs.identity_file)
    
    
def run_function(function, *args, **kwargs):
    output = function(*args, **kwargs)
    
    return output
    
def get_conf_files():

    #configurations
    zettaknight_globs.zfs_conf = _get_conf(zettaknight_globs.config_file_new)
    zettaknight_globs.zpool_conf = _get_conf(zettaknight_globs.pool_config_file)
    zettaknight_globs.zettaknight_conf = _get_conf(zettaknight_globs.zettaknight_config_file)

    
def get_active_zfs_info():
    
    zettaknight_globs.live_zpools = get_live_zpools()
    zettaknight_globs.live_datasets = get_live_datasets()
    
    
def import_config(file):
    ''' import a yaml configuration file, returns a dictionary '''
    
    with open(file, 'r') as myfile:   
        config = yaml.safe_load(myfile)
        
    return config
    
    
def _get_conf(config_file):

    config_dict = import_config(config_file)

    if 'defaults' in six.iterkeys(config_dict):
        s_defaults = set(config_dict['defaults'])

        for key in config_dict:
            s_config = set(config_dict[key])

            for property in s_defaults.difference(s_config):
                if property != 'defaults':
                    config_dict[key][property] = config_dict['defaults'][property]

        config_dict.pop('defaults')

    return config_dict
    
def get_live_zpools():
    '''retrieve all zpool defined on the filesystem, returns in list format'''
    
    zpool_list = []
    
    query = '/sbin/zpool list -H'
    zpool_query = zettaknight_utils.spawn_job2(query)
    stdout, stderr = zpool_query
    if stdout:
        for line in stdout.split('\n'):
            items = line.split('\t')
            zpool = items[0]
            if zpool:
                zpool_list.append(zpool)
    
    logger.debug('live zpools: {0}'.format(zpool_list))
    return zpool_list
    

def get_live_datasets():
    '''retrieve all datasets defined on the filesystem for each zpool, returns in list format'''
    
    dataset_list = []
    
    query = '/sbin/zfs list -H'
    datasets_query = zettaknight_utils.spawn_job2(query)
    stdout, stderr = datasets_query
    if stdout:
        for line in stdout.split('\n'):
            items = line.split('\t')
            dataset = items[0]
            if dataset:
                dataset_list.append(dataset)