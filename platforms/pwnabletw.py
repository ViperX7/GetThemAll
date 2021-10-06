import requests
from bs4 import BeautifulSoup
from writeupMgr.chall import Chall

base = "https://pwnable.tw"
__import__("os").system("clear")


def chall(id, name, desc, points, nc, links):
    data = {}
    conn = {}
    data['name'] = name
    data['id'] = int(id)
    data['desc'] = desc
    data['points'] = int(points)
    data['difficulty'] = None
    data['category'] = None
    data['img'] = None
    host, port = nc.strip().split(" ")[1:]
    conn['host'], conn['port'] = host, int(port)
    conn["passwd"] = None
    conn['type'] = "nc"
    data['conn'] = conn

    data["flag"] = "NA"
    data['urls'] = links
    data['files'] = []
    data['tags'] = []

    return Chall.from_dict(data)


def getChalls():
    page = requests.get(base + "/challenge/").content
    soup = BeautifulSoup(page, 'html.parser')
    items = soup.findAll('li', attrs={"class": "challenge-entry"})

    challsList = []
    for item in items:
        desc = item.find("div", {"class": "description"})
        id = item["id"].strip("challenge-id-")
        name = item.find("span", {"class": "tititle"}).text
        points = item.find("span", {"class": "score"}).text.strip(" pts")
        nc = [x.text for x in desc.find_all("code") if "nc chall" in x.text][0]
        links = [base + x["href"] for x in desc.find_all("a")]

        desc_msg = desc.find_all("p")
        msg = list(set([x.a.decompose() if x.a else x for x in desc_msg]))
        msg.remove(None)
        msg = [x.text for x in msg]
        msg.remove(nc)
        msg = "\n".join(msg)

        print("A")
        newchall = chall(id, name, msg, points, nc, links)
        challsList.append(newchall)
    return challsList
