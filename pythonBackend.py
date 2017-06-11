# for checking for compilation/syntax and some runtime errors
# (c) Alex Shukhman 03/24/17

import sys
try:
	import simplejson as json
except:
	import json

# Read
def readIn():
    lines = sys.stdin.readlines()
    # multiple lines --> lines[all]=lines json.loads(lines) returns a 
    return lines

def main():
    # Read input
    lines = readIn()

    # Parse
    #parse_out = parseLines(lines)

    # Return Using Print
    print(json.dumps({'success':True, 'lines':lines}))


# on call, start process
if __name__ == '__main__':
    main()
