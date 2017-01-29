var express = require('express');
var morgan = require('morgan');
var mongoose = require('mongoose');
var bodyParser = require('body-parser');
var api = express();
var jwt = require('jsonwebtoken'); // used to create, sign, and verify tokens
var config = require('./config'); // get our config file
var User = require('./api/models/user'); // get our mongoose model
// =======================
// configuration =========
// =======================
console.log('config api');
mongoose.connect(config.database); // connect to database
api.set('superSecret', config.secret); // secret variable
// use body parser so we can get info from POST and/or URL parameters
api.use(bodyParser.urlencoded({
	extended: false
}));
api.use(bodyParser.json());
// use morgan to log requests to the console
api.use(morgan('dev'));
// =======================
// routes ================
// =======================
// basic route
console.log('configged, now set up routes');
api.get('/', function (req, res) {
	res.send('Hello! The API is at http://localhost:' + apiport + '/api');
});
// API ROUTES -------------------
// we'll get to these in a second
// note: no view engine setup or favicon setup
module.exports = api;