import scraper
import helper


browser = scraper.initialise_browser()
ctf_challs = scraper.ctfd_scraper(browser)


if ctf_challs["name"]:
    name = ctf_challs["name"]
else:
    print("Name of challenge is required")
    exit(1)

if ctf_challs["desc"]:
    desc = ctf_challs["desc"]
    urls = helper.urlDetect(desc)
    if urls:
        for url in urls:
            if ctf_challs["links"]:
                if url not in ctf_challs["links"]:
                    ctf_challs["link"] += ',' + url
            else:
                ctf_challs["link"] = url

if ctf_challs["conn"]:
    connections = ctf_challs["conn.split(',')"]
    conn = [""]
    for connection in connections:
        conn.append(
            connection.replace('nc', '').strip(' ').replace(':', ' ').split(' '))
else:
    conn = ''
if ctf_challs["files"]:
    files = ctf_challs["files.split(',')"]
else:
    files = [""]
if ctf_challs["category"]:
    category = ctf_challs["category"]
else:
    category = ''
if ctf_challs["points"]:
    points = ctf_challs["points"]
else:
    points = ''
if ctf_challs["links"]:
    links = helper.sanitise(ctf_challs["links"])
else:
    links = ''
if ctf_challs["tags"]:
    tags = helper.sanitise(ctf_challs["tags"])
else:
    tags = ''

Readme = helper.genWriteup(name, conn, files, desc,
                           category, points, links, tags)
helper.prepare(name, Readme, category, files, conn)
