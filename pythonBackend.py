# for checking for compilation/syntax and some runtime errors
# (c) Alex Shukhman 03/24/17

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
import sys, time, subprocess, digitalocean

from digitalocean import SSHKey

try:
    import simplejson as json
except:
    import json

#############################################################

global pytoken
pytoken = 'b3b477b085ab490b0360a33df665fbcb07752051e08fd554debd16b7eaa9b51d'
global ssh_key
ssh_key ={'id': 'pykey',
          'fingerprint': '47:75:a3:5d:2c:e1:79:6b:29:61:33:a2:7d:4a:a9:50',
          'public_key': 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC8D2gvpLO6aUsaaYyGGOqU4WaQ7qCx0X+AVv+1D6eJRaCZyG05QvN/Zaymb7Uf/VDngX+8BNZAJgGGkMTHRp86yeurNSlYc7K6bLNOsbyhj/Vht0NaWm9zHHXLS4FXj09d/js2YjAPZXFIp/at1y1o9LaG0C9uaorxT8AhaQWfKhl7FmZ6FQUg8ukTWcUBFXzXECHQch+VCEhi8v49J5fwTDiVxVZ44o0n79P7tN/qhMtDNSnucWIHVHPaHHcjZkpznKLimaY2m9pmOYfNEUQEIhAFflOPrbMyF4dsDdluuf5ii3RPnzc2oA/Cg6ZNboOfA5bBGdNQbmZboW8kzP0n alex.jacob.shukhman@gmail.com',
          'name': 'pykey'}

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
                             region= 'nyc2',
                             image= 'ubuntu-16-04-x32',
                             size_slug='512mb',
                             ssh_keys = [ssh_key['public_key']],
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
    closeServer(d)
    return time.time()-t0

#162.243.252.100

# on call, start process
'''if __name__ == '__main__':
    main()'''
