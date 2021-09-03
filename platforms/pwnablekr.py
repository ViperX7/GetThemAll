import requests
from bs4 import BeautifulSoup
from writeupMgr.chall import Chall

base = "https://pwnable.kr/"


def chall(id, name):
    data = {}
    conn = {}
    data['name'] = name
    data['id'] = id
    data['desc'] = get_desc(id)
    data['points'] = None
    data['difficulty'] = None
    data['category'] = None
    data['img'] = get_img(name)

    conn['host'], conn['port'], conn['passwd'] = parse(data['desc'])
    conn['type'] = "ssh" if conn['passwd'] else "nc"
    data['conn'] = conn

    data["flag"] = "NA"
    data['urls'] = []
    data['files'] = []
    data['tags'] = []

    return Chall.from_dict(data)


def desc_process(desc):
    desc = desc.split("Download")[0].strip()
    desc = desc.split("Running at")[0].strip()
    desc = desc.split("ssh")[0].strip()
    desc = desc.replace("\n", "").replace("\x0d", "")
    return desc


def get_desc(id):
    url = base + 'playproc.php?no=' + str(id)
    page = requests.get(url).content
    soup = BeautifulSoup(page, 'lxml').find('textarea')
    desc = soup.text
    return desc


def get_img(name):
    fname = name + ".png"
    url = base + 'img/' + fname
    return url


def parse(desc):
    conninfo = desc.split("\n")[-1]
    pwd = None
    host = None
    port = -1
    if 'ssh' in conninfo:
        conninfo = conninfo.split(' ')
        host = list(set([x if "@" in x else None for x in conninfo]))
        host.remove(None)
        host = host[0]

        port = list(set([x if "-p" in x else None for x in conninfo]))
        port.remove(None)
        port = port[0].strip('-p')

        pwd = list(set([x if "pw:" in x else None for x in conninfo]))
        pwd.remove(None)
        pwd = pwd[0].split("pw:")[1].strip(")")

    elif 'nc' in conninfo:
        host, port = conninfo.split(" ")[-2:]
    else:
        print(desc)

    return host, int(port), pwd


def getChalls():
    page = requests.get(base + "play.php").content
    soup = BeautifulSoup(page, 'lxml')
    items = soup.findAll('figure')

    challsList = []
    for item in items:
        print("A")
        id = item.find('img')['onclick'].replace('onLayer(',
                                                 '').replace(");", '')
        id = int(id)
        newchall = chall(id, item.text.strip())
        challsList.append(newchall)
    return challsList
