// get an instance of mongoose and mongoose.Schema
var mongoose = require('mongoose');
var Schema = mongoose.Schema;
// set up a mongoose model and pass it using module.exports
module.exports = mongoose.model('Tasks', new Schema({
	name: String
	, lang: String
	, owner: String
	, task: {
		message_short: String
		, message_long: String
		, pet_code: String
	}
	, bounty: Number
	, date: {
		type: Date
		, default: Date.now
	}
}));