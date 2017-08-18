// get an instance of mongoose and mongoose.Schema
var mongoose = require('mongoose');
var Schema = mongoose.Schema;
// set up a mongoose model 
var Responses = new Schema({
	coder: String
	, code: String
	, lang: String
	, task_id: String
	, success: Boolean
	, created_at: {
		type: Date
	}
	, updated_at: {
		type: Date
	}
});
// middle ware in serial
Responses.pre('save', function (next) {
	now = new Date();
	this.updated_at = now;
	if (!this.created_at) {
		this.created_at = now;
	}
	var currentdate = new Date;
	this.date = currentdate.now;
	this.__v = this.__v + 1;
	next();
});
// Pass model using module.exports
module.exports = mongoose.model('Responses', Responses);