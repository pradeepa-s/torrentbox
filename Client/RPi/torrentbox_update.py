#!/usr/bin/python

import subprocess
import datetime

output_dir = "/mnt/external/rpi_movies"

def process_torrent_list(torrent_json):
	torr_list = torrent_json['torrents']

	torr_count = len(torr_list)

	for i in range(torr_count):
		process_torrent_record(torr_list[i])

		if(torrent_json['torrents'][i]['Action'] == 'Rem'): 
			torrent_json['torrents'][i]['Action'] = 'Deleted'
		else:
			torrent_json['torrents'][i]['Action'] = 'Processed'




	return torrent_json

def process_torrent_record(record):

	action = record['Action']
	val = record['Values']
	id = record['BTIH']
	start = record['Start']
	stop = record['Stop']

	record_dict.get(action, no_processing)(val,id,start,stop)

	return
	
def add_torrent(torrent,id,start,stop):
	
	subprocess.Popen('deluge-console "add -p ' + output_dir + ' ' + torrent + '"' , shell=True, executable="/bin/bash");

	return

def rem_torrent(torrent,id,start,stop):
	
	subprocess.Popen('deluge-console "rm ' + id.lower() + '"', shell=True);

	return

def no_processing(torrent,id,start,stop):
	return

def get_torrent_status():
	process = subprocess.Popen('deluge-console info', shell=True, executable="/bin/bash", stdout=subprocess.PIPE)
	val_tuple = process.communicate()
	string = val_tuple[0]
	
	if(len(string) == 0):
		string = 'No torrents'

	return string

def pause_torrent(torrent, id, start, stop):

	subprocess.Popen('deluge-console "pause ' + id.lower() + '"', shell=True);

	return 

def resume_torrent(torrent, id, start, stop):

	subprocess.Popen('deluge-console "resume ' + id.lower() + '"', shell=True);

	return 


def run_scheduler(torr_json):
	time_val = int(str(datetime.datetime.now().hour) + str(datetime.datetime.now().minute));
	
	torrents_list = torr_json['torrents']
	torr_count = len(torrents_list)

	pause = 0
	
	for i in range(torr_count):
		# Only run the schduler on added torrents
		if(torrents_list[i]['Action'] != 'Processed'):
			continue

		start_val = int(torrents_list[i]['Start'])
		stop_val = int(torrents_list[i]['Stop'])
		

		if(start_val > stop_val):
			if((time_val > stop_val) and (time_val < start_val)):
				pause = 1
			else:
				pause = 0

		elif(start_val < stop_val):
			if((time_val < stop_val) and (time_val >= start_val)):
				pause = 0
			else:
				pause = 1
		else:
			pause = 1

		if(pause == 1):
			if(torrents_list[i]['State'] != 'Paused'):
				pause_torrent(0, torrents_list[i]['BTIH'], 0, 0)
				torr_json['torrents'][i]['State'] = 'Paused' 
		else:
			if(torrents_list[i]['State'] != 'Resumed'):
				resume_torrent(0, torrents_list[i]['BTIH'], 0, 0)
				torr_json['torrents'][i]['State'] = 'Resumed' 

			
	return torr_json
		
 	
		

record_dict = { 'Add' 	: add_torrent,
		'Rem' 	: rem_torrent,
		'Pause'	: pause_torrent,
		'Resume': resume_torrent
		}		
