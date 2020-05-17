var express = require('express');
var router = express.Router();
var passport = require('passport');
var LocalStrategy = require('passport-local').Strategy;
var async = require('async');
var crypto = require('crypto');
var bcrypt = require('bcryptjs');
var nodemailer = require('nodemailer');

//Requiring user-schema for registering etc.
var User = require('../models/user');

//Handles the passport authentication methods
require('../config/passport.js')(passport, LocalStrategy);

// Register - GET 
router.get('/register', function(req, res){
	User.find().exec(function(err, result) {
	    if (err) return console.log(err)
		if (result.length>0) {
			req.flash('error_msg','Too many users are registered.');
			res.redirect('/users/login');
		} else {
			res.render('account/register', {number_of_users: result.length});
		}
		
	 })
});

// Register - POST
router.post('/register', function(req, res){
	var username = req.body.username;
	var password = req.body.password;
	var password2 = req.body.password2;

	// Validation
	req.checkBody('username', 'Username is required').notEmpty();
	req.checkBody('password', 'Password is required').notEmpty();
	req.checkBody('password2', 'Passwords do not match').equals(req.body.password);

	var errors = req.validationErrors();

	if(errors){
		res.render('register',{
			errors:errors
		});
	} else {
		var newUser = new User({
			username: username,
			password: password
		});

		User.createUser(newUser, function(err, user){
			if(err) throw err;
			console.log(user);
		});

		req.flash('success_msg', 'You are registered and can now login');

		res.redirect('/users/login');
	}
});

// Login - GET
router.get('/login', function(req, res){
	res.render('account/login');
});

// Login - POST
router.post('/login',
  passport.authenticate('local', {successRedirect:'/', failureRedirect:'/users/login',failureFlash: true}),
  function(req, res) {
	  res.redirect('/');
});

// Logout - GET
router.get('/logout', function(req, res){
	req.logout();

	req.flash('success_msg', 'You are logged out');

	res.redirect('/users/login');
});

module.exports = router;