#!/usr/bin/python

import argparse

def zettaknight_arguments():

    '''zettaknight argument parsing and help documentation'''

    try:
        parser = argparse.ArgumentParser(description='my parent description here')
        parser.add_argument('--suppress-mail', action='store_true', help = 'we send no email')
        
        subparsers = parser.add_subparsers()
        
        sub1 = subparsers.add_parser('status', help = 'check the status of zettaknight')
        sub1.add_argument('status', action = 'store_true', help = 'if set zettaknight checks status')
        
        sub3 = subparsers.add_parser('create', help = 'create a zfs zpool')
        sub3.add_argument('zpool name', help = 'name of the zpool to be created, i.e zfs_data')
        
        sub4 = subparsers.add_parser('maintain', help = 'zettaknight maintain run')
        sub4.add_argument('dataset', help = 'zfs dataset')
        
        sub5 = subparsers.add_parser('nuke', help = 'delete a zpool')
        sub5.add_argument('zpool', help = 'name of the zpool to delete')
        
        sub6 = subparsers.add_parser('enforce_config', help = '''
            enforce attributes defined in the zettaknight configuration file
            ''')
        sub6.add_argument('enforce_config', action = 'store_true', help = 'boolean, will ran when called')
        sub6.add_argument('--force', action = 'store_true', help = '''
            if set, zettaknight ignores if the configuration file has been modified
            and executes enforce_config
            ''')
            
        sub7 = subparsers.add_parser('enforce_zpool_config', help = '''
            enforce attributes defined in the zettaknight zpool configuration file
            ''')
        sub7.add_argument('--force', action = 'store_true', help = '''
            if set, zettaknight ignores if the zpool configuration file has been modified
            and executes enforce_zpool_config
            ''')
            
        sub7 = subparsers.add_parser('scrub', help = 'scrub a zpool')
        sub7.add_argument('zpool', help = 'zpool to be scrubbed')
        
        sub8 = subparsers.add_parser('sync_all', help = 'replicate all local snapshots to their defined remote targets')
        sub8.add_argument('sync_all_flag', action = 'store_true', help = 'boolean, will ran when envoked')
        sub8.add_argument('--parallel', dest = 'sync_all_parallel', action = 'store_true', help = 'by default, snapshots sync serially, if envoked, snapshots sync in parallel')
        
        sub9 = subparsers.add_parser('zfs_monitor', help = 'checks the health of all zfs filesystems defined on a machine')
        sub9.add_argument('monitor', action = 'store_true', help = 'boolean, will ran when envoked')
        
        sub10 = subparsers.add_parser('generate_perf_stats', help = 'write zpool iostat information to a file')
        sub10.add_argument('file', help = 'file to write zpool iostat information')
        
        sub11 = subparsers.add_parser('ssh_keygen', help = 'create a 4096 bit RSA key')
        sub11.add_argument('keyfile', help = 'location to write the key, i.e /tmp/mykey.key')
        
        sub12 = subparsers.add_parser('backup_luks_headers', help = '''
            Function to backup headers for currently defined LUKS devices. By default, headers are backed up to the
            Zettaknight store defined in configuration files. Target argument can be supplied to redirect where the
            headers are backed up to.
            ''')
        sub12.add_argument('directory', help = '''
            full path to directory where the luks headers are to be dumped. If empty, present working directory is
            assumed.
            ''')
        

        args = parser.parse_args()

        
    except Exception, e:
        raise Exception(e)
    
    return args
    
args = zettaknight_arguments()
print args
