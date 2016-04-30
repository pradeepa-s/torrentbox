#!/usr/bin/python

import subprocess

# Update the mount location of your HDD
MOUNT_LOCATION = '/mnt/external'

# Check whether the hard disk is mounted

def check_hdd_mount():
	mnt_check_process = subprocess.Popen('cat /proc/mounts', shell=True, stdout=subprocess.PIPE);
	sys_mounts_tuple = mnt_check_process.communicate();
	sys_mounts = sys_mounts_tuple[0];
	mount_index = sys_mounts.find(MOUNT_LOCATION , 0, len(sys_mounts));
	
	if(mount_index != -1):
		return 0;
	else:
		return -1;


#print check_hdd_mount()	
