from writeupMgr.chall import Chall
from GetThemAll.platforms import pwncollege
import os

chall = Chall.load('.')

level = 0
while not os.path.isfile('creds.py'):
    level += 1
    if level == 3:
        print('Cannot find credentials')
        exit()
    os.chdir('../')

if True:
    from writeupMgr.utils import fread
    creds = fread('creds.py')
    print(creds)
    exec(creds)
    ctf = pwncollege.pwncollege(URL, {"pass": password, "user": username})
    ctf.auth()
    ctf.startChall(chall.id)
