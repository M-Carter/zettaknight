#!/usr/bin/python

from subprocess import PIPE, Popen
import re
import traceback



##########################################################
#################### ZPOOLS #################################
##########################################################

def get_zpools():
    zpool_list = []
    
    try:
        pipe = Popen('zpool list -H', stdout = PIPE, shell = True)
        for line in pipe.stdout:
            elements = line.split()
            zpool = elements[0]
            zpool_list.append(zpool)
            
    except Exception, e:
        raise Exception(e)
        
    return zpool_list
        
        
def get_zpool_attributes(zpool):

    command = 'zpool get all -H {0}'.format(zpool)
    pipe = Popen(command, stdout = PIPE, shell = True)
    
    for line in pipe.stdout:
        elements = line.split()
        zpool = elements[0]
        property = elements[1]
        value = elements[2]
        
        if property == 'size':
            size = convert_to_bytes(value)
            
        if property == 'capacity':
            #remove % sign
            capacity = int(re.sub("[^0-9]", "", value))
            
        if property == 'free':
            free = convert_to_bytes(value)
            
        if property == 'allocated':
            allocated = convert_to_bytes(value)
            
        if property == 'fragmentation':
            #remove % sign
            frag = int(re.sub("[^0-9]", "", value))
        
    attributes = (zpool, size, capacity, free, allocated, frag)
        
    return attributes
    
    
def get_zpool_totals(zpool):
    
    total_quota_bytes = 0
    total_refquota_bytes = 0
    total_reservation_bytes = 0
    total_refreservation_bytes = 0


    attributes = get_zpool_attributes(zpool)
    
    total_size_bytes = attributes[1]
    total_capacity = attributes[2]
    total_free_bytes = attributes[3]
    total_allocated_bytes = attributes[4]
    frag = attributes[5]

    for dataset in datasets:
        #check to see if dataset is a child of the current zpool, if so continue
        dataset_parts = dataset.split('/')
        dataset_zpool = dataset_parts[0]
        
        if dataset_zpool == zpool:
    
            attributes = get_dataset_attributes(dataset)
            snapshots = get_snapshots(dataset)
            
            quota = attributes[6]
            refquota = attributes[7]
            reservation = attributes[8]
            refreservation = attributes[9]
            
            #don't add if quota is none or not an integer
            if quota != 'none':
                total_quota_bytes += quota
                
            if reservation != 'none':
                total_reservation_bytes += reservation
    
            #if attributes[1] == '0':
                #print attributes
                #print snapshots
                
    attributes = (total_size_bytes, total_allocated_bytes, total_free_bytes, total_quota_bytes,
                total_refquota_bytes, total_reservation_bytes, total_refreservation_bytes, frag)
        
    return attributes
    

##########################################################
################## DATASETS #################################
##########################################################
    
def get_datasets():
    dataset_list = []
    
    try:
        pipe = Popen('zfs list -H', stdout = PIPE, shell = True)
        for line in pipe.stdout:
            elements = line.split()
            dataset = elements[0]
            dataset_list.append(dataset)
            
    except Exception, e:
        raise Exception(e)
        
    return dataset_list
    
    
def get_dataset_attributes(dataset):

    command = 'zfs get all -H {0}'.format(dataset)
    pipe = Popen(command, stdout = PIPE, shell = True)
    
    for line in pipe.stdout:
        elements = line.split()
        dataset = elements[0]
        property = elements[1]
        value = elements[2]
        
        if property == 'quota':
            quota = convert_to_bytes(value)
            
        if property == 'refquota':
            refquota = convert_to_bytes(value)
            
        if property == 'reservation':
            reservation = convert_to_bytes(value)
            
        if property == 'refreservation':
            refreservation = convert_to_bytes(value)
            
        if property == 'compression':
            compression = value
            
        if property == 'used':
            used = convert_to_bytes(value)
            
        if property == 'available':
            available = convert_to_bytes(value)
            
        if property == 'usedbysnapshots':
            used_by_snapshots = convert_to_bytes(value)
            
        if property == 'usedbydataset':
            used_by_dataset = convert_to_bytes(value)
            
        if property == 'usedbychildren':
            used_by_children = convert_to_bytes(value)
            
        if property == 'compressratio':
            compression_ratio = value
            
    attributes = (dataset, used_by_children, used_by_dataset, used_by_snapshots,
                        compression, compression_ratio, quota, refquota, reservation, refreservation)
    
    return attributes
    
    
def get_snapshots(dataset):

    snapshots = []

    try:
        command = 'zfs list -r -t snapshot -o name -H {0}'.format(dataset)
        pipe = Popen(command, stdout = PIPE, shell = True)
        
        for line in pipe.stdout:
            elements = line.split()
            snapshot = elements[0]
            
            snapshots.append(snapshot)
            
    except Exeption, e:
        raise Exception(e)
        
    return snapshots


##########################################################
##################### UTILS #################################
##########################################################

    
def convert_to_bytes(string, base = 2):

    '''
    Takes a string and converts it to Bytes.
    1KB returns int 1024 Bytes.  Base take two arguments,
    2 or 10.  Base 2 for Megabytes, 10 for Mebbibytes
    '''
    
    if base == 2:
        conv = 1024
    if base == 10:
        conv = 1000
    
    try:
    
        if string not in ('none', '0'):
        
            #pull all non integer and decimal values
            a = re.sub("[^\d.]+", "", string)
            
            if a.isdigit():
                a = int(a)
            else:
                a = float(a)

            string = string.upper()
            b = re.sub("[^A-Z]", "", string)
        
            if b.startswith('K'):
                string = a * (conv ** 1)
                
            elif b.startswith('M'):
                string = a * (conv ** 2)
            
            elif b.startswith('G'):
                string = a * (conv ** 3)
            
            elif b.startswith('T'):
                string = a * (conv ** 4)
                
            elif b.startswith('P'):
                string = a * (conv ** 5)
                
            else:
                raise ValueError('invalid format for string: {0}'.format(string))
                    
    except Exception, e:
        raise Exception(e)
        
    return string
    
    
    
def convert_from_bytes(n, base = 2):

    if n == 0:
        return n
    
    if base == 2:
        conv = 1024
    if base == 10:
        conv = 1000
    
    try:
    
        suffix_list = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']

        index = 5
        
        while index > 0:
        
            size_full = conv ** index
            
            if n >= size_full:
                size = size_full
                suffix = suffix_list[index]
                break
                
            else:
                index -= 1
        
        n = n / size_full
        n = '{0}{1}'.format(n, suffix)
            
                    
    except Exception, e:
        raise Exception(e)
        
    return n
    
    
#START
try:
    datasets = get_datasets()
    zpools = get_zpools()
    
    for zpool in zpools:
        out = get_zpool_totals(zpool)
        
        print 'CAPACITY:', convert_from_bytes(out[0])
        print 'USED:', convert_from_bytes(out[1])
        print 'FREE:', convert_from_bytes(out[2])
        print 'TOTAL QUOTA:', convert_from_bytes(out[3])
        print 'TOTAL RESERVED:', convert_from_bytes(out[5])
        print 'FRAGMENTATION: {0}%'.format(out[7])
        
except:
    tb = traceback.format_exc()
    print tb
    #print('ERROR: {0}'.format(e))
        
        