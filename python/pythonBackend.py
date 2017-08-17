# for checking for compilation/syntax and some runtime errors
# (c) Alex Shukhman 2/28/17

############################################################################

# Info

'''
Build 0.0.0
Notes:
    Don't forget to pip install stuff.
    This is the only not-automated step (everything else should work out the box).
    
    All servers run on ubuntu-16-04-x32 slug at a size of 512mb.
    That should be more than enough space.
    To work with setup files, use (js)setup.sh. <- will offer different setups per language
    Do not do any server setup directly with Python, only with shell scripts.
	
    If using new libraries for import, update documentation accordingly.
    To Test Setup:
        1. Create JS file and parth file
        2. Run in Terminal:
            - python (or python3)
            - from pythonBackend import *
            - test(jsFilePath = 'route/to/file.js', pyFilePath = 'route/to/pythonmiddleware.py', parthFilePath = 'route/to/parthfile.parth', verbose = True) <- no attr results in testing of foo.js
    
    For Build 0.0.0:
        Languages Offered:
            - Javascript  
        Build Platforms:
            - .js: Nodejs JS Interpreter
pip: <- if running python3, command is pip3, not pip
    pip install -U python-digitalocean
    pip install -U paramiko
    pip install -U pysendfile
DigitalOcean Python Token:
    pyToken = b3b477b085ab490b0360a33df665fbcb07752051e08fd554debd16b7eaa9b51d <- do not use without my permission
To SSH to server (requires unix machine or git bash):
    cd path/to/smopapi
    ssh -i key root@[ip] -> ip being the server ip address
    
'''

############################################################################

# Imports

import os, sys, time, subprocess, socket, digitalocean, paramiko

import testframework # mostly for imports and toDict

from digitalocean import SSHKey

try:
    import simplejson as json
except:
    import json

############################################################################

# Globals (minimize use of globals)

global pytoken
pytoken = 'b3b477b085ab490b0360a33df665fbcb07752051e08fd554debd16b7eaa9b51d'

############################################################################

# Helper Functions

# Destroy Server
def closeServer(d):
    return d.destroy()

# Pre-Parsing
def parseLines(lines):
    writeFile(lines)
    return

# Checks if str is valid javascript file name
def isfiletype(s, blank):
    return "."+blank == s[-1*(len(blank)+1):-1]+s[-1]

# Parse Test Results
def parseout(everything):
    try:
        everything['success'] = True
        everything['out'] = testframework.toDict(everything['out'])
        failed_tests = []
        for key in everything['out'].keys():
            if everything['out'][key] == 'false': #test if any tests failed
                failed_tests.append(key)
                
        if everything['errors'] != '':
            everything['success'] = False
            
        if len(failed_tests) == 0:
            everything['test_errors'] = ''

        else:
            everything['success'] = False
            everything['test_errors'] = 'Tests failed = ' + str(failed_tests)
			everything['errors'] = 'Not all unit tests passed. Other Errors:'+everything['errors']
            
    except Exception as e:
        everything['success'] = False
        everything['errors'] = 'Test Error, please contact the owner of this task'
        everything['test_errors'] = 'Unsuccessful Testing, something may be wrong with the tests'

    return everything

# Read File
def readFile(file):
    with open(file, 'r') as f:
        return f.readlines()

# Read Input From NPM
def readIn():
    lines = json.dumps(sys.stdin.readlines())
    return json.loads(lines)

# Set Up Server and Run JS File
def runSetup(ip, ssh_key, jsFilePath, pyFilePath, parthFilePath, verbose):
    # connection setup
    connection = paramiko.SSHClient()
    connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if verbose:
        print('server aquired, running commands...')
    
    # connect -- try a maximum of maxTries times
    maxTries = 10 # hopfully doesn't take more than like 2 or 3
    tries = 0
    success = False
    while maxTries>tries:
        try:
            tries += 1
            if verbose:
                print('Try ' + str(tries))
            connection.connect(hostname=ip, username='root', key_filename='key')
            success = True
            break
        except Exception as e:
            # print(e)
            time.sleep(5) # give it a sec or two...

    # if it's just not working...        
    if not success:
        return '', 'failed to connect because '+str(e), ip # error

    # send all files including setup and run files
    filelist = [jsFilePath, pyFilePath, parthFilePath]
    for f in filelist:
        try:
            sendToIP(f, ip, verbose)
        except Exception as e:
            return '', 'Error with sending file: ' + str(e), ip # error
    if verbose:
        print('connected to server, running setup...')
    
    # setup and run on server
    try:
        scommands = readFile('jssetup.sh') # setup commands
    except:
        scommands = readFile('python/jssetup.sh')
        
    for command in scommands: # silent
        if verbose:
            print('executing '+ str(command))
        stdin, stdout, stderr = connection.exec_command(command)
        out = stdout.read().decode("utf-8").strip()
        #print(out)
        #print ("Errors")
        errors = stderr.read().decode("utf-8").strip()
        #print(errors)

    rcommands = ['ls -a', 'python testframework.py'] # run commands
    for command in rcommands:
        if verbose:
            print('executing '+ str(command))
        stdin, stdout, stderr = connection.exec_command(command)
        out = stdout.read().decode("utf-8").strip()
        if verbose:
            print(out)
        #print ("Errors")
        errors = stderr.read().decode("utf-8").strip()
    connection.close()
    return out, errors, ip

# FTP Local Files
def sendToIP(filename, ip, verbose):
    # set up
    PRIVATEKEY = 'key'
    user = 'root'
    server = ip
    port = 22
    paramiko.util.log_to_file("support_scripts.log")
    trans = paramiko.Transport((server,port))
    rsa_key = paramiko.RSAKey.from_private_key_file(PRIVATEKEY)

    # connect
    trans.connect(username=user, pkey=rsa_key)
    session = trans.open_channel("session")

    # ftp files
    sftp = paramiko.SFTPClient.from_transport(trans)
    if verbose:
        print('copying files...')
    if isfiletype(filename, 'js'):
        path = '/root/app.js' # call the script 'app.js'
    elif isfiletype(filename, 'py'):
        path = '/root/testframework.py' # call the test framework 'testframework.py'
    elif isfiletype(filename, 'parth'):
        path = '/root/tests.parth' # call the test file 'tests.parth'
    else:
        path = '/root/'+filename # in root directory
    localpath = './'+filename
    sftp.put(localpath, path)

    # close
    sftp.close()
    trans.close()
            
# Create Server
def spinupServer(token, ssh_key, verbose): # DO NOT RUN WITHOUT MY PERMISSION, THIS IS A PAID SERVICE, always close server when done
    # ask DigitalOcean.com to provision a server (d for droplet)
    d = digitalocean.Droplet(token=pytoken,
                             name='test'+token,
                             region= 'nyc3',
                             image= 26446785, #Ubuntu 17.04 x64
                                                 #manager = digitalocean.Manager(token = pytoken)
                                                 #manager.get_all_images()
                             size_slug='512mb',
                             ssh_keys = [ssh_key.id],
                             backups=True)
    d.create()

    # make sure the server is totally built
    while True:
        d.load()
        if d.ip_address!=None:
            if verbose:
                print('IP ' + str(d.ip_address) +
                      ' acquired, acquiring rest of server ...')
            break
    while True:
        if "completed" in str(d.get_actions()[0].status):
            break
    return d

# Write a File
def writeFile(lines):
    with open("python/foo.js", "w") as f:
        for line in lines:
            f.write(line)
    return

############################################################################

# Run Functions 

def test(jsFilePath='app.js', pyFilePath='testframework.py', parthFilePath='tests.parth', verbose = True):
    # ssh key get -- the key will work with the local files, do /not/ make new ones (aka, no ssh-keygen)
    ssh_key = digitalocean.Manager(token = pytoken).get_all_sshkeys()[0] # there should only be one

    # provision server then set it up and run code
    t0 = time.time()
    d = spinupServer("AJS", ssh_key, verbose)
    out, errors, ip = runSetup(d.ip_address, ssh_key, jsFilePath, pyFilePath, parthFilePath, verbose)
    
    '''try:
        raw_input('To close server press ENTER')
    except:
        input('To close server press ENTER')'''
    
    timeAJS = time.time()-t0
    # input('press enter, ip = '+str(ip))
    # destroy server and print operating cost (usually negligible)
    closeServer(d)
    # print('$'+str(round(.03*timeAJS/60/60,2))) # how much cash you owe me
    return {'_owed':'$'+str(round(.03*timeAJS/60/60,2)),
            'out': out,
            'errors': errors}
    
def main():
    # Read input
    lines = readIn()

    writeFile(lines)

    everything = test(jsFilePath='python/app.js', pyFilePath='python/testframework.py', parthFilePath='python/tests.parth', verbose = False)
    everything = parseout(everything)
    everything['lines'] = readFile('python/foo.js')
    
    # Return Using Print
    print(json.dumps(everything))

    return #EOF

# on call, start process
if __name__ == '__main__':
    main()
