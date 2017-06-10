# for checking for compilation/syntax and some runtime errors
# (c) Alex Shukhman 2/28/17

#############################################################

'''
Variables:
    lines = list object
    line = string object

DigitalOcean Python Token:
    pyToken = b3b477b085ab490b0360a33df665fbcb07752051e08fd554debd16b7eaa9b51d <- do not use without my permission
'''

#############################################################

# imports 
import sys, time, subprocess, digitalocean, platform

from digitalocean import SSHKey

try:
    import simplejson as json
except:
    import json

#############################################################

global pytoken
pytoken = 'b3b477b085ab490b0360a33df665fbcb07752051e08fd554debd16b7eaa9b51d'
global ssh_key
ssh_key ='ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDAIPY2/fM4To+t3NnyN18lrgdA//XMwh4oGWdhVw+cQiBOhZ0zlXRSkPCa+W3j0ORGNLfgIl0GTgOuMQOQLvEIyBuNlqEpWRQ2LfKuwJPs0Vo6blT+vVJl6vPHERA97Hoe4osN+DXFpzqdahLTWZEC37zy4bFySYwDLS+rhrS++Xo7cLB6q4+8I3n60/TcTN3uBh8AO0vRDA/8GEKqfc/jlXxg40o0/pmO7yYdSHqxDyDQibK2TSs7NUvuhxO5DT3IPR2EM7/lAIY5QRT902XcDt68BJ2M4JaqwSh5kl5b4AEQC8Hj7W2Dmes+Sq6Vby32VIDDsWUAGiKz6ycsjXx7 Dell User@ShukhmanPC'

# Read
def readIn():
    lines = json.dumps(sys.stdin.readlines())
    return json.loads(lines)

def main():
    # Read input
    lines = readIn()

    parse_out = parseLines(lines)

    # Return Using Print
    print(json.dumps({'success':True, 'lines':lines}))

def writeFile(lines):
    with open("foo.js", "w") as f:
        for line in lines:
            f.write(line)

def parseLines(lines):
    writeFile(lines)
	
def spinupServer(token): # DO NOT RUN WITHOUT MY PERMISSION, THIS IS A PAID SERVICE, always close server when done
    d = digitalocean.Droplet(token=pytoken,
                             name='test'+token,
                             region= 'nyc1',
                             image= 'ubuntu-16-04-x32',
                             size_slug='512mb',
                             ssh_keys = [ssh_key],
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
    t0 = time.time()
    d = spinupServer("AJS")
    runSetup(d.ip_address)
    try:
        raw_input('Press Enter')
    except:
        input('Press Enter')
    timeAJS = time.time()-t0
    closeServer(d)
    return '$'+str(round(.007*timeAJS/60/60,2)) # how much cash you owe me

def runSetup(ip):
    linesserver = ['sudo apt-get update',
               'sudo apt-get install nodejs',
               'nodejs app1.js', 'read -p "Press enter to continue"']
    linessh = ['ssh -i key '+ip+' "','"']
    linessh = [linessh[0]+'; '.join(linesserver)+linessh[1]]
    linesbat = ['bash -c "', '"']
    if platform.system() == "Windows":
        with open('jssetup.bat', 'w') as f:
            linesbat = [linesbat[0]+'; '.join(linessh)+linesbat[1]] #requires win10 bash
            f.writelines(linesbat)
        subprocess.call(['./jssetup.bat'])
    else:
        with open('jssetup.sh', 'w') as f:
            f.writelines(linessh)
            f.writelines(linesserver)
        subprocess.call(['./jssetup.sh'])
    

# on call, start process
'''if __name__ == '__main__':
    main()'''
