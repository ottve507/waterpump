//Load authentication strategies 
var User = require('../models/user');

module.exports = function(passport, LocalStrategy){

	passport.use(new LocalStrategy(
		function(username, password, done) {
			User.getUserByUsername(username, function(err, user){
				if(err) throw err;
				if(!user){
					return done(null, false, {message: 'Unknown User'});
				}

				User.comparePassword(password, user.password, function(err, isMatch){
					if(err) throw err;
					if(isMatch){
						return done(null, user);
					} else {
						return done(null, false, {message: 'Invalid password'});
					}
				});
			});
			}));

	passport.serializeUser(function(user, done) {
			done(null, user.id);
	});

	passport.deserializeUser(function(id, done) {
			User.getUserById(id, function(err, user) {
				done(err, user);
			});
	});

	// Load the auth variables (For Facebook)
	var configAuth = require('../config/main');

}
