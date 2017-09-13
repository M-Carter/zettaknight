#!/bin/bash

#reinstall zfs

set -e

echo -e "\nremoving zfs"
yum remove zfs -y 

echo -e "\nremoving broken kernel objects"
for i in $(ls /lib/modules); do 
    echo $i
    
    dir1="/lib/modules/${i}/extra"
    
    if [ -d $dir1 ]; then
        ls $dir1 
        rm -rf ${dir1}*
    fi
        
    dir2="/lib/modules/${i}/weak-updates"
    
    if [ -d $dir2 ]; then
        ls $dir2
        rm -rf ${dir2}*
    fi

done


yum reinstall --nogpgcheck spl spl-dkms -y 
yum reinstall --nogpgcheck zfs-dkms -y 
yum install --nogpgcheck zfs -y

