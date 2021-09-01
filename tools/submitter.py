#!/bin/python
from GetThemAll.platforms import ctfd
from creds import *
import os

ctf = ctfd.CTFd(URL, {"pass": password, "user": username})
ctf.auth()

challs = ctf.challenges()
pwd = os.getcwd()
with open(pwd + "/.challenge_name") as f:
    identifier = f.read()
with open(pwd + "/flag_txt") as f:
    flag = f.read().strip("\n").strip(" ")
print("[*] " + identifier + ": " + flag + " Submitting Flag", end="")
res = challs[identifier].submit(flag)
if res:
    print("\r[ + ] " + identifier + ": " + flag + " Accepted        ", end="")
else:
    print("\r[ - ] " + identifier + ": " + flag + " Rejected       ", end="")
