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