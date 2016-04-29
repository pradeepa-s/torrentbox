#!/usr/bin/python

import os_support
import server_comm
import torrentbox_update
import syslog
import time

def execute_app():

	error_state = 0
	torrent_update = False
		
	# Check whether hdd is mounted
	if(os_support.check_hdd_mount() == -1):
		syslog.syslog(syslog.LOG_INFO, 'Hard Disk Not Mounted')
		error_state = 1

	# Get the torrent list	
	if(error_state == 0):
		torr_json = server_comm.get_torrent_list();

		if(torr_json != -1):
			torrent_update = True;

	
	# Update the torrent list in torrent client
	if(torrent_update == True):
		#print "Got torrents"
		torr_json = torrentbox_update.process_torrent_list(torr_json);
		

	# Update current torrent status to server
	tstatus = torrentbox_update.get_torrent_status()
	server_comm.send_torrent_status(tstatus)
	
	
	# Process the torrent scheduling tasks (ie: pause, resume)
	if(torr_json != -1):
		torr_json = torrentbox_update.run_scheduler(torr_json)

	# Update the torrent list in the server
	if(torrent_update == True):
		server_comm.update_server_side_list(torr_json)

	time.sleep(10)

	return


def app_entry():
	
	while True:
		execute_app()

app_entry()
