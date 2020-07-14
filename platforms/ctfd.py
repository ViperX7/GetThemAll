#!/bin/env python3

import os
import requests
import json
import argparse
import re
import sys
# from config import *

# os.system('clear')


class ConnError(Exception):
    pass


class CTFd:
    def __init__(self, url, creds={}):
        # Basic Variables
        self.username = None
        self.email = None
        self.password = None
        if creds != {}:
            self.creds(creds)
        # CTF url and connection checking
        self.url = url
        # Create a session
        self.session = requests.session()
        self.session.headers.update(
            {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0'})

       # Checking Connection
        print("[*] Checking Connection to " + self.url, end="")
        resp = self.session.get(self.url)
        if resp.ok:
            print("\tSuccess\r[+]")
        else:
            print("\tFailed\r[-]")
            print("[?] Are you sure the URL to the CTF is correct")
            print("\tAlso check weater connection is available")
            print("[X] "+str(resp.status_code))
            exit(1)
        self.__challenges = None
        self.__users = None
        self.__teams = None
        self.__scoreboard = None
        self.isstarted = None

    def info(self, context=None):
        s = self.session
        resp = s.get(self.url+"/api/v1/users/me")
        data = resp.json()['data']

        if not data:
            print("Please Login To Get Current Status")
            return
        if context is None:
            print("Username: " + data['name'])
            print("Score   : " + str(data['score']))
            print("Place   : " + str(data['place']))
        elif context == "--":
            print("Available info : ")
            for x in data:
                print("  " + x)
        elif context == "-":
            print("====Data===\n\n")
            for x in data:
                if data[x]:
                    print("  [>] " + x + " : " + str(data[x]))
        else:
            print(context + str(self.data[context]))

    def creds(self, authdata):
        if 'user' in authdata:
            self.username = authdata['user']
        elif 'email' in authdata:
            self.email = authdata['email']
        else:
            print("You Must To Provide The Registered Username or Email")
            exit()
        if 'pass' in authdata:
            self.password = authdata['pass']
        else:
            print("Please provide the password")
            exit()

    # A way to provide authentication data after the ctfd object is created
    # Or Login with another Account
    def login(self, authdata):
        self.creds(authdata)
        self.auth()

    # Authenticate user and perform some checks
    def auth(self):
        s = self.session
        if self.username:
            identifier = self.username
        else:
            identifier = self.email

        print("[*] Loading login page " + self.url, end="")
        resp = s.get(self.url+"/login")
        if resp.ok:
            print("\tSuccess\r[+]")
            print("\t[*] CSRF Token : ", end="")
            nonce = resp.text.split('name="nonce" value="')[1].split('"')[0]
            if len(nonce) % 64 == 0:
                print("\tok\r\t[+]")
            else:
                print("\tnok " + str(len(nonce)) + "\r\t[-]")
        else:
            print("\tFailed\r[-]")
            exit(1)

        loginData = {"name": identifier,
                     "password": self.password, "nonce": nonce}

        print("[*] Authenticating " + self.url, end="")
        resp = s.post(self.url+"/login", data=loginData)
        self.isstarted = True
        if resp.ok:
            print("\tAuthenticated\r[+]")
        elif resp.status_code == 403:
            if "has ended" in resp.text:
                print("\tAuthenticated\r[+]")
                print("\t[*] Seems Like CTF has ended")
            elif "not started" in resp.text:
                print("\tAuthenticated\r[+]")
                print("\t[*] Seems Like you are early CTF not started yet")
                self.isstarted = False
        else:
            print("\tFailed\r[-]")
            print(resp.status_code)
            exit(1)
        self.sync()

    # Get all the information about the user
    # TODO get all the information and use a user object to store this info
    def sync(self):
        s = self.session
        resp = s.get(self.url+"/api/v1/users/me")
        # print(resp.text)
        data = resp.json()['data']
        self.username = data['name']
        self.email = data['email']

    def scoreboard(self, upto=0):
        resp = self.session.get(self.url + "api/v1/scoreboard")
        entry = resp.json()["data"]
        self.__scoreboard = entry
        print("\t\tPlace\t\t\tName\t\t\t\tScore\n")
        for x in entry:
            print("\t\t" + str(x["pos"]) + "\t\t\t" +
                  x["name"] + "\t\t\t\t" + str(x["score"]))

##############################################################################
# Challenges, Teams, and Users are cached after the first request
# so subsequent call to these methods only returns the cached requests
##############################################################################
    def users(self, search=None):
        if self.__users is None:
            resp = self.session.get(self.url + "/api/v1/users")
            usrs = resp.json()['data']
            self.__users = users(self.session, self.url)
            for user in usrs:
                self.__users.add(user)
        return self.__users

    def challenges(self):
        # If CTF not started no challenges can be fetched so return blank list
        if self.isstarted is False:
            return []
        if self.__challenges is None:
            self.__challenges = challenges(self.session, self.url)
            resp = self.session.get(self.url+"/api/v1/challenges")
            prblms = resp.json()["data"]
            for prblm in prblms:
                self.__challenges.add(prblm)
        return self.__challenges

    def teams(self):
        if self.__teams is None:
            self.__teams = teams(self.session, self.url)
            resp = self.session.get(self.url+"/api/v1/teams")
            tems = resp.json()["data"]
            for tem in tems:
                self.__teams.add(tem)
        return self.__teams
##############################################################################


class users:
    def __init__(self, session, url):
        self.__session = session
        self.__url = url
        self.__ulist = []

    def add(self, usr):
        if type(usr) == dict or type(usr) == int:
            new_user = user(usr, self.__session, self.__url)
        elif type(usr) == user:
            new_user = usr
        self.__ulist.append(new_user)

    def __getitem__(self, key):
        result = None
        if type(key) == int:
            result = self.__ulist[key]
        if type(key) == str:
            print("[*] Searching..." + str(key), end="")
            for x in self.__ulist:
                if key.lower() == x.name.lower():
                    print("\t\t\t Found\r[+]")
                    result = x
        if result is None:
            print("\t\t\t Not Found\r[-]")
        return result

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        out = []
        for x in self.__ulist:
            out.append(x.name)
        return str(out)

    def find(self, search):
        output = users(self.__session, self.__url)
        for user in self.__ulist:
            if search.lower() in user.name.lower():
                output.add(user)
            elif user.affiliation and search.lower() in user.affiliation:
                output.add(user)
            elif user.website and search.lower() in user.website.lower():
                output.add(user)
            elif user.country and search.lower() in user.country.lower():
                output.add(user)
        return output


class user:
    def __init__(self, prop, session, url):
        self.__session = session
        self.__url = url
        if type(prop) != int:
            self.__id = prop["id"]
            self.name = prop["name"]
            self.website = prop["website"]
            self.affiliation = prop["affiliation"]
            self.country = prop["country"]

        else:
            self.__id = prop
            self.name = None
            self.website = None
            self.affiliation = None
            self.country = None

        self.isloaded = False

    def load(self):
        resp = self.__session.get(self.__url+"/api/v1/users/"+str(self.__id))
        prop = resp.json()["data"]
        self.name = prop["name"]
        self.website = prop["website"]
        self.affiliation = prop["affiliation"]
        self.country = prop["country"]

        self.score = prop["score"]
        self.place = prop["place"]
        self.isloaded = True

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if self.name is None:
            self.load()
        return str(self.name)

    def view(self):
        if self.isloaded == False:
            self.load()
        print("Username: " + self.name)
        print("Score: " + str(self.score) + "pts @ " + str(self.place))
        if self.affiliation:
            print("Affiliation: " + self.affiliation + ", " + self.country)
        if self.website:
            print("Website:" + self.website)

    def solves(self):
        resp = self.__session.get(
            self.__url+"/api/v1/users/"+str(self.__id)+"/solves")
        solves = resp.json()["data"]
        result = []
        for solve in solves:
            res = {}
            if solve["team"] is not None:
                res["team"] = team(solve["team"], self.__session, self.__url)
            res["date"] = solve["date"]
            res["type"] = solve["type"]

            solve["challenge"]["id"] = solve["challenge_id"]
            solve["challenge"]["tags"] = None
            solve["challenge"]["type"] = None
            res["challenge"] = challenge(
                solve["challenge"], self.__session, self.__url)
            result.append(res)
        return result


class teams:
    def __init__(self, session, url):
        self.__session = session
        self.__url = url
        self.__tlist = []

    def add(self, nteam):
        if type(nteam) == dict or type(nteam) == int:
            new_team = team(nteam, self.__session, self.__url)
        elif type(nteam) == team:
            new_team = nteam
        self.__tlist.append(new_team)

    def __getitem__(self, key):
        if type(key) == int:
            result = self.__tlist[key]
        if type(key) == str:
            result = None
            for x in self.__tlist:
                if key.lower() == x.name.lower():
                    result = x
        return result

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        out = []
        for x in self.__tlist:
            out.append(x.name)
        return str(out)

    def find(self, search):
        output = users(self.__session, self.__url)
        for user in self.__tlist:
            if search.lower() in user.name.lower():
                output.add(user)
            elif user.affiliation and search.lower() in user.affiliation:
                output.add(user)
            elif user.website and search.lower() in user.website.lower():
                output.add(user)
            elif user.country and search.lower() in user.country.lower():
                output.add(user)
        return output


class team:
    def __init__(self, prop, session, url):
        self.__session = session
        self.__url = url
        if type(prop) != int:
            self.__id = prop["id"]
            self.name = prop["name"]
            self.website = prop["website"]
            self.affiliation = prop["affiliation"]
            self.country = prop["country"]
            self.captain = user(prop["captain_id"], self.__session, self.__url)

        else:
            self.__id = prop
            self.name = None
            self.website = None
            self.affiliation = None
            self.country = None

        self.isloaded = False

    def load(self):
        resp = self.__session.get(self.__url+"/api/v1/teams/"+str(self.__id))
        prop = resp.json()["data"]
        self.name = prop["name"]
        self.website = prop["website"]
        self.affiliation = prop["affiliation"]
        self.country = prop["country"]
        self.members = users(self.__session, self.__url)
        for x in prop["members"]:
            self.members.add(x)
        self.captain = user(prop["captain_id"], self.__session, self.__url)

        self.score = prop["score"]
        self.place = prop["place"]
        self.isloaded = True

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if self.name is None:
            self.load()
        return str(self.name)

    def view(self):
        if self.isloaded == False:
            self.load()
        print("Team: " + self.name)
        print("Score: " + str(self.score) + "pts @ " + str(self.place))
        if self.affiliation:
            print("Affiliation: " + self.affiliation + ", " + self.country)
        if self.website:
            print("Website:" + self.website)
        print("Members: ")
        for x in self.members:
            print(x)


class challenges:
    def __init__(self, session, url):
        self.__sess = session
        self.__url = url
        self.__clist = []
        self.__categories = []

    def __getitem__(self, key):
        if type(key) == int:
            result = self.__clist[key]
        if type(key) == str:
            result = None
            for x in self.__clist:
                if key == x.name:
                    result = x
        return result

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        out = []
        for x in self.__clist:
            out.append(x.name)
        return str(out)

    def add(self, chall):
        if type(chall) == challenge:
            new_chall = chall
        else:
            new_chall = challenge(chall, self.__sess, self.__url)
        self.__clist.append(new_chall)
        if new_chall.category not in self.__categories:
            self.__categories.append(new_chall.category)

    def category(self, search=None):
        if search is None:
            return self.__categories
        else:
            c_in_cat = challenges(self.__sess, self.__url)
            for chall in self.__clist:
                if search in chall.category:
                    c_in_cat.add(chall)
            return c_in_cat


class challenge:
    def __init__(self, prop, session, url):
        self.__sess = session
        self.__url = url
        if type(prop) != int:
            self.__id = prop["id"]
            self.category = prop["category"]
            self.name = prop["name"]
            self.value = prop["value"]
            self.tags = prop['tags']
            self.type = prop["type"]
        else:
            self.__id = prop
        self.__isloaded = False

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if self.name is None:
            self.load()
        return self.name

    def __getitem__(self, key):
        return getattr(self, key)

    def load(self):
        resp = self.__sess.get(self.__url+"/api/v1/challenges/"+str(self.__id))
        chall = resp.json()["data"]
        self.category = chall["category"]
        self.name = chall["name"]
        self.tags = chall["tags"]
        self.value = chall["value"]
        self.files = chall["files"]
        self.description = chall["description"]
        self.solves = chall["solves"]
        self.hints = chall["hints"]
        self.__isloaded = True

    def view(self):
        print("=> " + self.name + "\t\t" + "(" + self.category + ")")
        if self.__isloaded is False:
            self.load()
        print("Description:\n\t\t" + self.description)
        if len(self.files) > 0:
            print("Downloads:" + str(len(self.files)))
        print("Solves: " + str(self.solves))
        if self.hints:
            print("hint available")
        for t in self.tags:
            print(t, end=", ")

    # TODO Check if in conflict with self.solves
    def solves(self):
        resp = self.__sess.get(
            self.__url+"/api/v1/challenges/"+str(self.__id)+"/solves")
        solves = resp.json()["data"]
        result = []
        for solve in solves:
            res = {}
            if "user" in solve["account_url"]:
                res["user"] = user(solve["account_id"],
                                   self.__sess, self.__url)
            else:
                res["team"] = team(
                    solve["account_id"], self.__sess, self.__url)
            res["date"] = solve["date"]
            result.append(res)
        return result

    def __get_token(self):
        resp = self.__sess.get(self.__url+"/challenges")
        try:
            csrf = resp.text.split('csrf_nonce = "')[1].split('"')[0]
        except IndexError:
            csrf = resp.text.split("csrfNonce': \"")[1].split('"')[0]
        return csrf

    def submit(self, flag):
        csrf = self.__get_token()
        resp = self.__sess.post(self.__url+"api/v1/challenges/attempt",
                                json={"challenge_id": self.__id,
                                      "submission": flag},
                                headers={"CSRF-Token": csrf},)
        if resp.status_code != 200:
            print("Something Went Wrong")
        if resp.json()["data"]["status"] == "correct":
            return True
        else:
            return False

#
# sectf = CTFd(URL)
# sectf.creds({"user": username, "email": email, "pass": password})
# sectf.auth()
# sectf.scoreboard()
# print()
# ch = sectf.challenges()["API-only XSS"]
# print(ch.solves()[0]["user"].view())
#
# team.load()
# team.members[0].load()
# print(team.members)
#

# sectf.users()
# print(sectf.email)
# print(s.get(URL+"/api/v1/users/me").text)


# auth(URL,username, password)


# "/api/v1/users/me"
# "/api/v1/users/me/solves"
# "/api/v1/teams/me"
# "/api/v1/scoreboard"
# "/api/v1/challenges/"+challid
# "/api/v1/challenges/attempt"
# "/api/v1/challenges"
