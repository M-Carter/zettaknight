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