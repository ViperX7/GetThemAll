from creds import *
import ctfd
import helper
import os

os.system("clear")


auctf = ctfd.CTFd(URL, {"pass": password, "user": username})
auctf.auth()

challenges = auctf.challenges()
for challenge in challenges:
    files = []
    challenge.load()

    if challenge.name:
        name = challenge.name
    else:
        print("Name of challenge is required")
        exit(1)
    if challenge.description:
        desc = challenge.description
    #     urls = helper.urlDetect(desc)
    #     if urls:
    #
    #         links = ""
    #         for url in urls:
    #             if challenge.links:
    #                 if url not in challenge.links:
    #                     link += ',' + url
    #             else:
    #                 link = url
    #
    # if challenge.conn:
    #     connections = challenge.conn.split(',')
    #     conn = []
    #     for connection in connections:
    #         conn.append(
    #             connection.replace('nc', '').strip(' ').replace(':', ' ').split(' '))
    # else:
    #     conn = ''
    if challenge.files:
        for file in challenge.files:
            files.append(URL+file)
    else:
        files = []
    if challenge.category:
        category = challenge.category
    else:
        category = ''
    if challenge.value:
        points = challenge.value
    else:
        points = ''
    # if challenge.links:
    #     links = sanitise(challenge.links)
    # else:
    #     links = ''
    if challenge.tags:
        tags = helper.sanitise(challenge.tags)
    else:
        tags = ''

    conn = ""
    links = ""
    Readme = helper.genWriteup(
        name, conn, files, desc, category, points, links, tags)
    helper.prepare(name, Readme, category, files, conn)
    print("making")
