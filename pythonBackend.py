# for checking for compilation/syntax and some runtime errors
# (c) Alex Shukhman 2/28/17

import sys, json, numpy as np, subprocess as sp

# Read
def readIn():
    lines = sys.stdin.readlines()
    # multiple lines --> lines[all]=lines json.loads(lines) returns a 
    return json.loads(lines)

def main():
    # Read input
    lines = readIn()

    # Parse
    parse_out = parseLines(lines)

    # Return Using Print
    print(parse_out)

# Parser Logic Main
def parseLines(lines):
	bash_command('a="Apples and oranges" && echo "${a/oranges/grapes}"')
	errorOut = {error: False}
    return json.dumps(errorOut, ensure_ascii=False)

# Execute Bash Command
def bash_command(cmd):
	subprocess.Popen(cmd, shell=True, executable='/bin/bash')

# on call, start process
if __name__ == '__main__':
    main()
