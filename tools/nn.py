import ctfd
import helper
import os
from creds import *

# os.system("clear")

ctf = ctfd.CTFd(URL, {"pass": password, "user": username})
ctf.auth()
