//db connection
var dbUserDev = 'posttokenUser';
var dbPassDev = 'lazarusD!ck';
module.exports = {
	'secret': 'w00Tsmop1'
	, 'database_dev': 'mongodb://' + dbUserDev + ':' + dbPassDev + '@ds145128.mlab.com:45128/smop'
}; // secret: used to create and verify JSON Web Tokens