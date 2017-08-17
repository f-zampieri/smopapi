import re, ast, json, subprocess

def toDict(s):
    return ast.literal_eval(s)

def readFile(f):
    #returns a list of lines
    with open(f, 'r') as file:
        lines = file.readlines()
    return lines

def getLineInfo(line):
    #some wonky behavior with javascripts, lists and arrays all exists, that needs to be figured out
    try:
        data = re.findall(r"function\s(.*?)\s?(\(.*?\))\s?returns\s?(.*?)\s?;", line)[0]
        return data
    except IndexError:
        return

def createjs(lines):
    js = '\nresults = {\n"function name (args) = expected": "result"'
    for line in lines:
        info = getLineInfo(line)
        if info != None:
            js+='\n, "'+info[0]+info[1]+'= '+info[2]+'"'+': JSON.stringify('+info[0]+info[1]+'==='+info[2]+')'
    js += '\n}\nconsole.log(results);'
    return js

def getOutputs(js):
    with open('jsmiddleware.js', 'w') as f:
        for lines in readFile('app.js'):
            f.write(lines) # copy and paste original file
        for lines in js:
            f.write(lines) # add test cases
    process = subprocess.Popen('node jsmiddleware.js', stdout = subprocess.PIPE)
    outputs, err = process.communicate()
    if err:
        print(err)
    return outputs

filelines = readFile('tests.parth')
js = createjs(filelines)
results = getOutputs(js)
print (toDict(results.decode('utf-8')))
