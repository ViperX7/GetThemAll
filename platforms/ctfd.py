#!/bin/env python3

import re
import argparse
import json
import requests

import os
os.system('clear')

username = "meme"
email = "mimem79882@bizcomail.com"
password = "meme"
URL = "https://ctf.0x00sec.org"

class ConnError(Exception):
    pass

class CTFd:
    def __init__(self, url):
        self.username = None
        self.email = None
        self.password = None


        self.url = url
        # Create a session
        self.session = requests.session()
        # Checking Connection
        print("[*] Checking Connection to " + self.url, end="")
        resp = self.session.get(self.url)
        if resp.ok:
            print("\tSuccess\r[+]")
        else:
            print("\tFailed\r[-]")
            exit(1)

    def info(self, context=None):
        s = self.session
        resp = s.get(self.url+"/api/v1/users/me")
        data = resp.json()['data']

        if not data:
            print("Please Login To Get Current Status")
            return
        if context == None:
            print("Username: " + data['name'])
            print("Score   : " + str(data['score']))
            print("Place   : " + str(data['place']))
        elif context == "--":
            print("Available info : " )
            for x in data:
                print("  " + x)
        elif context == "-":
            print("====Data===\n\n" )
            for x in data:
                if data[x]:
                    print("  [>] " + x + " : " + str(data[x]))
        else:
            print(context + str(self.data[context]))



    def users(self,search=None):
        s = self.session
        resp = s.get(self.url + "/api/v1/users")
        users = resp.json()['data']
        if not search:
            print("====Data===\n\n" )
            for user in users:
                for x in user:
                    if user[x]:
                        print("  [>] " + x + " : " + str(user[x]))
        else:
            for user in users:
                for x in user:
                    if   str(search) in str(user[x]) :
                        print(user)
            print('done')

    def listchall()





    def creds(self, authdata):
        if 'user' in authdata:
            self.username = authdata['user']
        elif 'email' in authdata:
            self.email = authdata['email']
        else:
            print("You Have To Provide Either The Registered Username or Email")
            exit()
        if 'pass' in authdata:
            self.password = authdata['pass']
        else:
            print("Please provide the password")
            exit()


    def login(self, suthdata):
        self.creds(authdata)
        self.auth()


    def sync(self):
        s = self.session
        resp = s.get(self.url+"/api/v1/users/me")
        data = resp.json()['data']
        self.username =data['name']
        self.email =['email'] 

    def auth(self):
        s = self.session
        if self.username:
            identifier = self.username
        else:
            idntifier = self.email

        print("[*] Loading login page " + self.url, end="")
        resp = s.get(self.url+"/login")
        if resp.ok:
            print("\tSuccess\r[+]")
            print("\t[*] CSRF Token : ", end="")
            nonce = resp.text.split('name="nonce" value="')[1].split('"')[0]
            if len(nonce) == 64:
                print("\tok\r\t[+]")
        else:
            print("\tFailed\r[-]")
            exit(1)

        loginData = {"name": identifier, "password": self.password, "nonce": nonce}

        print("[*] Authenticating " + self.url, end="")
        resp = s.post(
            self.url+"/login", data=loginData)
        if resp.ok:
            print("\tAuthenticated\r[+]")
        else:
            print("\tFailed\r[-]")
            print(resp.status_code)
            exit(1)
            print("\tAuthenticated\r[+]")
        self.sync()


sectf = CTFd(URL)
sectf.creds({"user":username,"email":email,"pass":password})
sectf.auth()
sectf.users('meme')
# print(s.get(URL+"/api/v1/users/me").text)



# auth(URL,username, password)


# "/api/v1/users/me"
# "/api/v1/teams/me"
# "/api/v1/challenges"
# "/api/v1/scoreboard"
# "/api/v1/users/me/solves"
# "/api/v1/scoreboard"
# "/api/v1/challenges/"+challid
# "/api/v1/challenges/attempt"
