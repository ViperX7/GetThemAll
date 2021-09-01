from GetThemAll.platforms import ctfd
from creds import *

ctf = ctfd.CTFd(URL, {"pass": password, "user": username})
ctf.auth()
