var mongoose = require('mongoose');
var bcrypt = require('bcryptjs');

// User Schema
var UserSchema = mongoose.Schema({
	username: {
		type: String,
		index:true
	},
	password: {
		type: String
	}
});
UserSchema.index({username: 'text'});

//Makes it possible to use the "User"-model in other places. Also declare variable for later.
var User = module.exports = mongoose.model('User', UserSchema);

//Function for adding new user.
module.exports.createUser = function(newUser, callback){
	bcrypt.genSalt(10, function(err, salt) {
		bcrypt.hash(newUser.password, salt, function(err, hash) {
			newUser.password = hash;
			newUser.save(callback);
		});
	});
}

//Function for finding one user.
module.exports.getUserByUsername = function(username, callback){
	var query = {username: username};
	User.findOne(query, callback);
}

//Finding one user by id
module.exports.getUserById = function(id, callback){
	User.findById(id, callback);
}


//Function for comparing passwords.
module.exports.comparePassword = function(candidatePassword, hash, callback){
	bcrypt.compare(candidatePassword, hash, function(err, isMatch) {
    	if(err) throw err;
    	callback(null, isMatch);
	});
}
