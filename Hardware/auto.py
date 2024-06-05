import urllib.request
import os
import time
from subprocess import call

path='/home/nomir/Desktop/Project/'

time.sleep(5)
host='http://google.com'
try:
    urllib.request.urlopen(host)
    status = "Connected"
except:
    status = "Not connected"

if status == "Connected":
    print(status)
    PATH1 = os.path.join(path, 'testpothole_1.py')
    exec(open(PATH1).read())
else:
    print(status)
    exit()
    #PATH2 = os.path.join(path, 'shutdown.py')
    #exec(open(PATH2).read())
