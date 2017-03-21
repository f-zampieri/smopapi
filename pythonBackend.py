# for checking for compilation/syntax and some runtime errors
# (c) Alex Shukhman 2/28/17

import sys, json

# Read
def readIn():
    lines = sys.stdin.readlines()
    # multiple lines --> lines[all]=lines json.loads(lines) returns a 
    return json.loads(lines)

def main():
    # Read input
    #lines = readIn()

    # Parse
    #parse_out = parseLines(lines)

    # Return Using Print
    print(True)#parse_out)


# on call, start process
if __name__ == '__main__':
    main()
