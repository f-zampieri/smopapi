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
var Testuser = require('./api/models/testuser') // get mongoose model
var User = require('./api/models/user'); // get mongoose model
var UserInfo = require('./api/models/userinfo'); // get mongoose model
var Task = require('./api/models/task'); // get mongoose model
var Response = require('./api/models/response'); // get mongoose model
// =======================
// configuration =========
// =======================
var port = process.env.PORT || 3001; // used to create, sign, and verify tokens
mongoose.Promise = require('bluebird');
mongoose.Promise = global.Promise;
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
	// create a user
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
app.post('/newuser_test', function (req, res) {
	// create a user
	var nick = new Testuser({
		name: req.body.name
		, password: req.body.password
		, salt: req.body.salt
	});
	// save the sample user
	nick.save(function (err) {
		if (err) throw err;
		console.log('User saved successfully');
		res.json({
			success: true
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
apiRoutes.post('/authenticate_test', function (req, res) {
	// find the user
	Testuser.findOne({
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
// save response
apiRoutes.post('/post_ResponseSave', (req, res) => {
	Response.findOne({
		task_id: req.body.id
		, coder: req.headers['x-access-name']
	}, (err, response) => {
		if (err) throw err;
		if (!response) {
			var new_response = new Response({
				coder: req.headers['x-access-name']
				, code: req.body.data
				, lang: 'js'
				, task_id: req.body.id
				, success: false
			});
			new_response.save(function (err) {
				if (err) throw err;
				console.log('New response saved successfully');
				res.json({
					success: true
				});
			});
		}
		else {
			response.code = req.body.data;
			response.save((err, result) => {
				if (err) throw err;
				console.log('updated response');
				res.json({
					success: true
					, result: result
				});
			});
		}
	});
});
// route to parse and check code for standard issues
apiRoutes.post('/post_codeCheck', function (req, res) {
	console.log('AJS api init codeCheck');
	var pyshell = new shell('python/pythonBackend.py');
	Task.findById(req.body.id, "task.unit_tests", (err, tests) => {
		// sends a message to the Python script via stdin
		if (!tests || !tests.task.unit_tests) {
			tests = '';
			console.log('no tests found');
		}
		else tests = tests.task.unit_tests;
		pyshell.send(JSON.stringify([req.body.code, tests]));
		pyshell.on('message', function (message) {
			// receives python print statement 
			message = JSON.parse(message);
			if (message.success == 'true') {
				Task.findById(req.body.id, (err, task) => {
					task.success = true
					task.save((err, result) => {
						if (err) throw err;
					});
				});
				Response.findOne({
					task_id: req.body.id
					, coder: req.headers['x-access-name']
				}, (err, response) => {
					if (err) throw err;
					response.success = true;
					response.save((err, result) => {
						if (err) throw err;
					})
				});
			}
			else {
				Task.findById(req.body.id, (err, task) => {
					task.success = false
					task.save((err, result) => {
						if (err) throw err;
					});
				});
				Response.findOne({
					task_id: req.body.id
					, coder: req.headers['x-access-name']
				}, (err, response) => {
					if (err) throw err;
					response.success = false;
					response.save((err, result) => {
						if (err) throw err;
					})
				});
			}
			res.json({
				pySuccess: message.success
				, data: message.errors
			});
		});
		// end the input stream and allow the process to exit
		pyshell.end(function (err) {
			if (err) throw err;
			console.log('py is finished');
		});
	});
});
// route to get user info
apiRoutes.get('/get_info', function (req, res) {
	var name = req.headers['x-access-name'];
	var typeuser = req.headers['coder_owner']
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
				if (object.info.typeuser) {
					res.json({
						success: true
						, message: 'info acquired'
						, info: object.info
					});
				}
				else {
					res.json({
						success: true
						, message: 'no info found'
						, info: '//this is where you edit your info'
					});
				}
			}
			else {
				res.json({
					success: true
					, message: 'no info found'
					, info: '//this is where you edit your info'
				});
			}
		}
	});
});
// Get the Task Feed (Coder and Owner)
apiRoutes.get('/get_feed', (req, res) => {
	var name = req.headers['x-access-name'];
	var typeuser = req.headers['coder_owner'];
	if (typeuser == 'coder') {
		Task.find({
			lang: req.headers['lang']
		}, (err, result) => {
			if (err) throw err;
			if (result != []) {
				res.json({
					success: true
					, result: result
				});
			}
			else {
				res.json({
					success: true
					, result: 'No Tasks Found'
				});
			}
		});
	}
	else if (typeuser == 'owner') {
		Task.find({
			owner: name
		}, (err, result) => {
			if (err) throw err;
			if (result != []) {
				res.json({
					success: true
					, result: result
				});
			}
			else {
				res.json({
					success: true
					, result: 'No Tasks Found'
				});
			}
		});
	}
});
// Create a new task
apiRoutes.post('/post_newtask', function (req, res) {
	// create a task
	var task = new Task({
		name: req.body.name
		, lang: req.body.lang
		, owner: req.headers['x-access-name']
		, task: {
			message_short: req.body.task_message_short
			, message_long: req.body.task_message_long
			, pet_code: req.body.task_pet_code
			, unit_tests: req.body.task_unit_tests
		}
		, bounty: req.body.bounty
	});
	// save the sample user
	task.save(function (err) {
		if (err) throw err;
		console.log('Task saved successfully');
		res.json({
			success: true
		});
	});
});
// Get a Single Task
apiRoutes.get('/get_singletask', (req, res) => {
	if (req.headers['coder_owner'] == 'owner') {
		Task.find({
			_id: req.headers['id']
		}, (err, result) => {
			if (err) throw err;
			console.log('got singletask');
			res.json({
				success: true
				, result: result
				, mtype: 'json'
			});
		});
	}
	else {
		Response.findOne({
			coder: req.headers['x-access-name']
			, task_id: req.headers['id']
		}, "code", (err, resultOut) => {
			console.log('result out:', resultOut);
			if (err) throw err;
			if (!resultOut) {
				Task.find({
					_id: req.headers['id']
				}, (err, result) => {
					if (err) throw err;
					console.log('got singletask');
					res.json({
						success: true
						, result: result
						, mtype: 'json'
					});
				});
			}
			else {
				res.json({
					success: true
					, result: resultOut.code
					, mtype: 'code'
				});
			}
		});
	}
});
// Get Task Status
apiRoutes.get('/get_taskStatus', (req, res) => {
	console.log('getting task status');
	Response.findOne({
		task_id: req.headers['id']
	}, (err, result) => {
		if (err) {
			res.json({
				success: false
				, result: err
			});
		}
		else if (!result) {
			res.json({
				success: true
				, result: 'not started'
			});
		}
		else {
			Response.findOne({
				task_id: req.headers['id']
				, success: true
			}, (err, result) => {
				if (err) {
					res.json({
						success: false
						, result: err
					});
				}
				else if (!result) {
					res.json({
						success: true
						, result: 'in progress'
					});
				}
				else {
					res.json({
						success: true
						, result: 'done'
					});
				}
			});
		}
	});
});
// Create a new task
apiRoutes.post('/post_updatetask', function (req, res) {
	// create a task
	var task = Task.findOne({
		_id: req.body.id
	}, (err, task) => {
		if (err) {
			res.json({
				success: false
				, result: err
			});
		}
		task.name = req.body.name;
		task.lang = req.body.lang;
		task.task.message_short = req.body.task_message_short;
		task.task.message_long = req.body.task_message_long;
		task.task.pet_code = req.body.task_pet_code;
		task.task.unit_tests = req.body.task_unit_tests;
		task.bounty = req.body.bounty;
		task.save((err, result) => {
			if (err) throw err;
			console.log('updated task');
			res.json({
				success: true
				, result: result
			});
		});
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
app.listen(port, "0.0.0.0");
console.log('Magic happens at http://localhost:' + port);