function a(a1, a2) { // sanity test
	return a1 + a2;
}
var b = (b1) => { // different function format
	return b1 * 3;
}
var c = (c1) => { // recursive
	if (c1 === Math.pow(c1, 2)) return c1;
	else return c(c1 - 1);
}
results = {
"function name (args) = expected": "result"
, "a('a', 'b')= 'ab'": JSON.stringify(a('a', 'b')==='ab')
, "a(1,2)= 3": JSON.stringify(a(1,2)===3)
, "b(3)= 9": JSON.stringify(b(3)===9)
, "c(3)= 1": JSON.stringify(c(3)===1)
, "c(6)= 1": JSON.stringify(c(6)===1)
}
console.log(results);