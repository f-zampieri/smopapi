# for checking for compilation/syntax and some runtime errors
# (c) Alex Shukhman 2/28/17

#############################################################

'''
Variables:
    lines = list object
    line = string object

pip:
    pip install -U python-digitalocean
    pip install -U paramiko

DigitalOcean Python Token:
    pyToken = b3b477b085ab490b0360a33df665fbcb07752051e08fd554debd16b7eaa9b51d <- do not use without my permission
'''

#############################################################

# imports 
import os, sys, time, subprocess, digitalocean, platform, paramiko

from digitalocean import SSHKey

try:
    import simplejson as json
except:
    import json

#############################################################

global pytoken
pytoken = 'b3b477b085ab490b0360a33df665fbcb07752051e08fd554debd16b7eaa9b51d'

# Read
def readIn():
    lines = json.dumps(sys.stdin.readlines())
    return json.loads(lines)

def main():
    # Read input
    lines = readIn()

    # Return Using Print
    print(json.dumps({'success':True, 'lines':lines}))

def writeFile(lines):
    with open("foo.js", "w") as f:
        for line in lines:
            f.write(line)

def parseLines(lines):
    writeFile(lines)
	
def spinupServer(token, ssh_key): # DO NOT RUN WITHOUT MY PERMISSION, THIS IS A PAID SERVICE, always close server when done
    d = digitalocean.Droplet(token=pytoken,
                             name='test'+token,
                             region= 'nyc1',
                             image= 'ubuntu-16-04-x32',
                             size_slug='512mb',
                             ssh_keys = [ssh_key.id],
                             backups=True)
    d.create()
    
    while True:
        d.load()
        if d.ip_address!=None:
            print('IP: '+str(d.ip_address))
            break
    while True:
        if "completed" in str(d.get_actions()[0].status):
            break
    return d

def closeServer(d):
    return d.destroy()

def test():
    # ssh key create
    ssh_key = digitalocean.Manager(token = pytoken).get_all_sshkeys()[0] # there should only be one
    # get ready... get set... go!
    t0 = time.time()
    d = spinupServer("AJS", ssh_key)
    runSetup(d.ip_address, ssh_key)
    try:
        raw_input('Press Enter')
    except:
        input('Press Enter')
    timeAJS = time.time()-t0
    closeServer(d)
    return '$'+str(round(.007*timeAJS/60/60,2)) # how much cash you owe me

def runSetup(ip, ssh_key):
    # connection setup
    connection = paramiko.SSHClient()
    connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print('connecting...')
    # connect
    connection.connect( hostname=ip, username='root', key_filename='key' )
    print('connected')

    commands = ['jssetup.sh']
    for command in commands:
        print('executing '+ str(command))
        stdin, stdout, stderr = connection.exec_command(command)
        print (stdout.read())
        print ("Errors")
        print (stderr.read())
    connection.close()
    

# on call, start process
'''if __name__ == '__main__':
    main()'''
