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
import sys, time, subprocess, digitalocean

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

    parse_out = parseLines(lines)

    # Return Using Print
    print(json.dumps({'success':True, 'lines':lines}))

def writeFile(lines):
    with open("foo.js", "w") as f:
        for line in lines:
            f.write(line)

def parseLines(lines):
    writeFile(lines)
	
def spinupServer(token, slug): # DO NOT RUN WITHOUT MY PERMISSION, THIS IS A PAID SERVICE, always close server when done
    d = digitalocean.Droplet(token=pytoken,
                             name='test'+token,
                             region= 'nyc2',
                             image= slug,
                             size_slug='512mb',
                             backups=True)
    d.create()
    
    while True:
        a = d.get_actions()
        if "completed" in str(a[0].status):
            break
    return d

def closeServer(d):
    return d.destroy()

def timer():
    with open ("slugs.txt", "r") as slugs:
        slugs = slugs.readlines()
    times = {}
    for slug in slugs:
        slug = slug[1:-2]
        print(slug)
        t0 = time.time()
        try:
            closeServer(spinupServer("AJS", slug))
            print('pass')
            times[slug] = time.time()-t0
        except:
            print('fail')
            times[slug] = 404
    return times
    
# on call, start process
'''if __name__ == '__main__':
    main()'''
