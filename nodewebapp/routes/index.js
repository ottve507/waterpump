var express = require('express');
var router = express.Router();
const request = require('request');
var jwt = require('jsonwebtoken');
var User = require('../models/user');


/*
	This file both includes routes to views, and GET/POST routest that a user can make.
*/

var ip_address = "http://localhost:5000"

// Route for homepage (when logged in)
router.get('/', ensureAuthenticated, function(req, res){
	res.render('index');
});

// Check water level - GET request initiated in index.ejs and executed in python's main.py.
router.get('/check_water_level', ensureAuthenticated, function(req, res){
	
	//Options to be included in request
	const options = {
	    url: ip_address + '/water_level_call',
	    method: 'GET',
	    headers: {
	        'Accept': 'application/json',
	        'Accept-Charset': 'utf-8',
	        'User-Agent': 'my-water-level'
	    }
	};
	
	//API request
	request(options, function(response, resp, body){
		try {
			let json = JSON.parse(body);
		    console.log(json);
			res.send(json['water_level']);
		} catch (e) {
			res.send("Unable to load water level");
			console.log("Unable to load water level");
		}
	});

});

// Stop motor - GET request initiated in index.ejs and executed in python's main.py.
router.get('/stop_pump', ensureAuthenticated, function(req, res){
	
	//Options to be included in request
	const options = {
	    url: ip_address + '/stop_pump_call',
	    method: 'GET',
	    headers: {
	        'Accept': 'application/json',
	        'Accept-Charset': 'utf-8',
	        'User-Agent': 'stop-motor'
	    }
	};
	
	//API request to be made.
	request(options, function(response, resp, body){
		try {
			let json = JSON.parse(body);
	    	console.log(json);
			res.send("Stopped motor");
		} catch (e) {
			res.send("Unable to stop motor");
			console.log("Unable to stop motor");
		}
	});

});

// Restart server - GET request initiated in index.ejs and executed in python's main.py.
router.get('/restart_server', ensureAuthenticated, function(req, res){
	
	//Options to be included in request
	const options = {
	    url: ip_address + '/restart_server_call',
	    method: 'GET',
	    headers: {
	        'Accept': 'application/json',
	        'Accept-Charset': 'utf-8',
	        'User-Agent': 'restart-server'
	    }
	};
	
	//API request to be made.
	request(options, function(response, resp, body){
		try {
			let json = JSON.parse(body);
	    	console.log(json);
			res.send("Server restarted");
		} catch (e) {
			res.send("Unable to restart server");
			console.log("Unable to restart server");
		}
	});

});

// Stop server - GET request which is not initiated anywhere (only emergencies)
router.get('/stop_server', ensureAuthenticated, function(req, res){
	
	//Options to be included in request
	const options = {
	    url: ip_address + '/stop_server_call',
	    method: 'GET',
	    headers: {
	        'Accept': 'application/json',
	        'Accept-Charset': 'utf-8',
	        'User-Agent': 'restart-server'
	    }
	};
	
	//API request to be made.
	request(options, function(response, resp, body){
		try {
			let json = JSON.parse(body);
	    	console.log(json);
			res.send("Server stopped");
		} catch (e) {
			res.send("Unable to stop server");
			console.log("Unable to stop server");
		}
	});

});

// Stop motor - POST request initiated in index.ejs and executed in python's main.py.
router.post('/start_pump_time', ensureAuthenticated, function(req, res){
	
	//Options for API-call
	const options = {
	    url: ip_address + '/start_pump_time_call',
	    method: 'POST',
	    headers: {
	        'Accept': 'application/json',
	        'Accept-Charset': 'utf-8',
	        'User-Agent': 'my-post-level'
	    },
		json: req.body //Information being sent from index.ejs
	};
		
	//Options to be included in request
	request(options, function (error, response, body) {  
        try {
			//Print the Response
        	console.log(body);
			res.send("Started the motor");
		} catch (e){
			console.log("Something went wrong in the node app");
			res.send("Unable to start motor");
		}
	});

});


//Function that is used in the beginning of certain routes to ensure user is authenticated.
function ensureAuthenticated(req, res, next){
	if(req.isAuthenticated()){
		return next();
	} else {
		req.flash('error_msg','You are not logged in');
		res.redirect('/users/login');
	}
}


module.exports = router;