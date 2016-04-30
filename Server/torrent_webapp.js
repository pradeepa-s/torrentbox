var express = require('express');
var app = express();

var magnets = new Array();
var torrent_status = 'Not available';
var number_of_magnets = 0;
var magnetJSON = { torrents: [] };
var get_torrent_pending = false;

// Please setup your own password
var PASSWORD = 'password';

// Please setup the port of your choice
var LISTEN_PORT = 8080;

// Add a torrent to the list
app.get('/addTorrent/:auth/:magnet/:start/:stop', function(req, res){


	if(req.params.auth == PASSWORD){
		var main_str = req.params.magnet;
		var start_pos = main_str.search("btih:") + 5;
		var stop_pos = main_str.search("&dn");

		if(start_pos == -1 || stop_pos == -1){
			ret = '-1';
		}
		else{
			var btih = main_str.slice(start_pos, stop_pos);

			magnetJSON.torrents.push({"Action":"Add","Values":req.params.magnet,"BTIH":btih,"Start":req.params.start,"Stop":req.params.stop,"State":"NA"});

			get_torrent_pending = true;
			ret = '0';
		}
	}
	else{
		ret = '-1';
	}

	number_of_magnets = magnetJSON.torrents.length;

	res.send(ret);
});

// Change the torrent state to remove
app.get('/remTorrent/:auth/:id', function(req, res){
	
	if(req.params.auth == PASSWORD){
		if((req.params.id > number_of_magnets) || (req.params.id <= 0)){
			res.send("-1");
		}
		else{
			magnetJSON.torrents[req.params.id - 1].Action = "Rem";
			get_torrent_pending = true;
			res.send("Torrent #" + req.params.id + " state changed to remove");
		}
	}
	else{
		res.send("-1");
	}

	
});

// Get torrent list
app.get('/getTorrent', function(req, res){
	
	if(magnetJSON.torrents.length > 0){
		res.send(magnetJSON);
		get_torrent_pending = false;
	}
	else{	
		res.send("-1");
	}

});

// Submit torrent status
app.post('/submitStatus', function(req, res){

	req.on('data', function(chunk){
		torrent_status = chunk.toString();

	});
	
	res.send('0');
});

// Get torrent status
app.get('/getStatus', function(req, res){
	res.send(torrent_status);
});

// Update full torrent list by user
app.post('/fullUpdate/:jsonlist', function(req, res){
	get_torrent_pending = true;
	magnetJSON = JSON.parse(req.params.jsonlist);
	res.send("0");

});

// Update full torrent list by RPi
app.post('/fullUpdatePi', function(req, res){
	if(get_torrent_pending == false){
		req.on('data', function(chunk) {
			magnetJSON = JSON.parse(chunk.toString());
		});
		res.send("0");
	}
	else{
		res.send("-1");
	}
});

app.listen(LISTEN_PORT);
