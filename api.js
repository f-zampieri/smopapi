// =======================
// get the packages we need ============
// =======================
var express = require('express');
var shell = require('python-shell');
var app = express();
var crypto = require('crypto');
var bodyParser = require('body-parser');
var morgan = require('morgan');
var mongoose = require('mongoose');
var jwt = require('jsonwebtoken'); // used to create, sign, and verify tokens
var config = require('./config'); // get our config file
var User = require('./api/models/user'); // get mongoose model
var UserInfo = require('./api/models/userinfo'); // get mongoose model
// =======================
// configuration =========
// =======================
var port = process.env.PORT || 3001; // used to create, sign, and verify tokens
mongoose.Promise = require('bluebird');
mongoose.connect(config.database_dev); // connect to database
app.set('superSecret', config.secret); // secret variable
// use body parser so we can get info from POST and/or URL parameters
app.use(bodyParser.urlencoded({
	extended: false
}));
app.use(bodyParser.json());
// use morgan to log requests to the console
app.use(morgan('dev'));
// =======================
// routes ================
// =======================
// create user
app.post('/newuser', function (req, res) {
	// create a sample user
	var nick = new User({
		name: req.body.name
		, password: req.body.password
		, salt: req.body.salt
		, admin: req.body.admin
	});
	var data = new UserInfo({
		name: req.body.name
		, info: {}
	});
	// save the sample user
	nick.save(function (err) {
		if (err) throw err;
		data.save(function (err) {
			if (err) throw err;
			console.log('User saved successfully');
			res.json({
				success: true
			});
		});
	});
});
// API ROUTES -------------------
// apiRoutes are routes to helper functions /only/ do not call apiRoutes functions from outside the API
var apiRoutes = express.Router();
apiRoutes.get('/', function (req, res) {
	res.json({
		message: 'Welcome to the smop. API.'
	});
});
// =======================
// authentication ========
// =======================
// authentication script
apiRoutes.post('/authenticate', function (req, res) {
	// find the user
	User.findOne({
		name: req.body.name
	}, function (err, user) {
		if (err) throw err;
		if (!user) {
			res.json({
				success: false
				, message: 'Authentication failed. User not found.'
			});
		}
		else if (user) {
			// check if password matches
			var hash = crypto.createHmac('sha512', user.salt);
			hash.update(req.body.password);
			var value = hash.digest('hex');
			if (user.password != value) {
				res.json({
					success: false
					, message: 'Authentication failed. Wrong password.'
				});
			}
			else {
				// if user is found and password is right
				// create a token
				var token = jwt.sign(user, app.get('superSecret'), {
					expiresIn: 1440 * 60 // expires in 24 hours
				});
				// return the information including token as JSON
				res.json({
					success: true
					, message: 'Enjoy your token!'
					, token: token
				});
			}
		}
	});
});
// route middleware to verify a token
apiRoutes.use(function (req, res, next) {
	//console.log('running middleware');
	// check header or url parameters or post parameters for token
	var token = req.body.token || req.query.token || req.headers['x-access-token'];
	// decode token
	if (token) {
		// verifies secret and checks exp
		jwt.verify(token, app.get('superSecret'), function (err, decoded) {
			if (err) {
				//console.log('jwt not authenticated');
				return res.json({
					success: false
					, message: 'Failed to authenticate token.'
				});
			}
			else {
				// if everything is good, save to request for use in other routes
				//console.log(jwt);
				req.decoded = decoded;
				next();
			}
		});
	}
	else {
		// if there is no token
		// return an error
		//console.log('jwt not provided');
		return res.status(403).send({
			success: false
			, message: 'No token provided.'
		});
	}
});
apiRoutes.get('/checkToken', function (req, res) {
	console.log('running checkToken');
	res.json({
		success: true
	});
});
// route to parse and check code for standard issues
apiRoutes.post('/post_codeCheck', function (req, res) {
	console.log('AJS api init codeCheck');
	var pyshell = new shell('python/pythonBackend.py');
	// sends a message to the Python script via stdin
	console.log("AJS REQ CODE:\n" + req.body.code);
	pyshell.send(req.body.code);
	pyshell.on('message', function (message) {
		// receives python print statement 
		message = JSON.parse(message);
		console.log(message);
		res.json({
			success: message.success
			, data: req.body.code
		});
	});
	// end the input stream and allow the process to exit
	pyshell.end(function (err) {
		if (err) throw err;
		console.log('py is finished');
	});
});
// route to get user info
apiRoutes.get('/get_info', function (req, res) {
	var name = req.body.name || req.query.name || req.headers['x-access-name'];
	UserInfo.findOne({
		name: name
	}, function (err, object) {
		if (err) throw err;
		if (!object) {
			res.json({
				success: false
				, message: 'User not found'
			});
		}
		else if (object) {
			if (object.info) {
				res.json({
					success: true
					, message: 'info acquired'
					, info: object.info
				});
			}
			else if (!object.info) {
				res.json({
					success: true
					, message: 'no info found'
					, info: '//this is where you edit your info'
				});
			}
		}
	});
});
// apply the routes to our application with the prefix /api
app.use('/api', apiRoutes);
app.on('uncaughtException', function (err) {
	console.error(err);
	console.log("api Error, Node NOT Exiting...");
});
// start the server ======
// =======================
app.listen(port);
console.log('Magic happens at http://localhost:' + port);