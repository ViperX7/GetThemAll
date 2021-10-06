import requests
from writeupMgr.chall import Chall
from bs4 import BeautifulSoup

__import__('os').system('clear')

URL = "https://pwnable.xyz/"


def chall(id, name, points, desc, nconn, author, solves, file):
    data = {}
    conn = {}
    data['name'] = name
    data['id'] = int(id)
    data['desc'] = desc
    data['points'] = int(points)
    data['difficulty'] = None
    data['category'] = None
    data['img'] = None

    nconn = nconn.replace(" ", "").split(":")
    conn['host'], conn['port'] = [nconn[0], int(nconn[1])]
    conn['type'] = "nc"
    data['conn'] = conn

    data["flag"] = "NA"
    data['urls'] = []
    data['files'] = [{"url": URL[:-1] + file, "name": file.split("/")[-1]}]
    data['tags'] = []

    return Chall.from_dict(data)


def getChalls():
    page = requests.get(URL + "challenges/")
    html = page.content
    soup = BeautifulSoup(html, 'lxml')
    challenges = soup.findAll("div", attrs={"class": "modal fade"})
    challList = []
    challenges = challenges[:-2]
    for challenge in challenges:
        head = challenge.find("div", attrs={"class": "card-header d-flex"})
        head = head.findAll("div")
        name = head[0].text.strip()
        points = head[1].text.strip()
        desc = challenge.find("div", attrs={"class": "card-body"}).text.strip()
        foot = challenge.findAll("div", attrs={"class": "card-header"})[1]
        foot = foot.findAll("div")
        nconn, author, file, solves = [""] * 4
        id = challenge.find('form')['action'].split("/")[-2]
        for entry in foot:
            if "svc" in entry.text:
                nconn = entry.text.strip()
            elif "Author" in entry.text:
                author = entry.text.strip().strip("Author: ")
            elif "Solves" in entry.text:
                solves = entry.text.strip().strip("Solves: ")
            elif "download" in entry.text:
                file = entry.find("a")["href"]
        new_chall = chall(id, name, points, desc, nconn, author, solves, file)
        challList.append(new_chall)
    return challList
