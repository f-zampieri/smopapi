/* Task Task1 was posted by alexshukhman on Thu Aug 17 2017. Task1 has defined the task as such:
This is the first task, everything is already done for you.
Good Luck. */
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