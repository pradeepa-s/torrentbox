import requests
import json

# Set the server address here
SERVER_ADD = 'http://54.191.41.142:8080'

GET_TORRENT = '/getTorrent'
FULL_UPDATE_PI = '/fullUpdatePi'
SUBMIT_STATUS = '/submitStatus'

# Get the torrent list

def get_torrent_list():
	try:
		req = requests.get(SERVER_ADD+GET_TORRENT);

		if(req.text != -1):
			return req.json();
		else:
			return -1;

	except requests.exceptions.RequestException as e:
		return -1

# Submit the updated JSON

def update_server_side_list(torr_json):
	try:
		req = requests.post(SERVER_ADD + FULL_UPDATE_PI, data=json.dumps(torr_json))
	
		if(req.text == -1):
			return -1
		else:
			return 0

	except requests.exceptions.RequestException as e:
	
		return -1


# Submit the info of current torrents in list

def send_torrent_status(tstatus):
	try:
		req = requests.post(SERVER_ADD + SUBMIT_STATUS, data = tstatus)
	
		if(req.text == -1):
			return -1
		else:
			return 0

	except requests.exceptions.RequestException as e:
		return -1
