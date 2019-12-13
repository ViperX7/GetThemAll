#!/bin/python3
import argparse
import os


def sanitise(inp):
    seperators = [' ', ',', '\n']
    if type([]) != type(inp):
        inp = [inp]
    for sep in seperators:
        if len(inp) != 1:
            break
        inp = inp[0].split(sep)
    return inp


def download(files):
    import subprocess
    files = sanitise(files)
    for link in files:
        filename = link.split('/')[-1].split('?')[0]
        subprocess.call("wget --no-check-certificate -O" +
                        filename + ' ' + link, shell=True)


def urlDetect(str):
    import re
    regex = r'^(([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))?'
    links = re.findall(regex, str)
    return links


def genWriteup(name, nc='', files='', desc='', category='', pts='', links='', tags=''):
    Readme = ""
    Readme += '# ' + name + '\n'

    # Category and points Handelling
    if category == '':
        category = '--category--'
    if pts == '':
        pts = '---'
    Readme += '> ' + str(category) + ' | ' + str(pts) + ' points\n'
    Readme += '--------------------' + '\n\n'

    if tags:
        for tag in tags:
            Readme += 'Link + ' + tag + '  '
        Readme += '\n\n'
    Readme += '## Problem Statement\n'

    # Description Handelling
    while desc.find('\n\n') != -1:
        desc = desc.replace('\n\n', '\n')
    desc = desc.strip('\n').replace('\n', '  \n> ')
    Readme += '> ' + desc + '  \n'

    if nc:
        Readme += '> * Connect using: nc' + nc[0] + ' ' + nc[1] + '\n'
    if links:
        for link in links:
            Readme += '> * [*' + link + '*](' + link + ')\n'
    if files:
        for file in files:
            filename = file.split('/')[-1].split('?')[0]
            Readme += '> * [*' + filename + '*](./' + filename + ')\n'
    return Readme


def prepare(name, Readme, category='.', files='', conn=''):
    base_dir = os.getcwd()
    if category:
        if category not in os.listdir():
            os.mkdir(category)
        os.chdir(category)
    name = name.replace(' ', '_')
    banned_chars = ['/']
    for char in banned_chars:
        name.replace(char, '-')
    os.mkdir(name)
    os.chdir(name)

    # Netcat connections mannagement
    if conn:
        conn_scpt = '#!/bin/bash\n'
        conns = conn
        for conn in conns:
            ip, port = conn
            conn_scpt += 'nc ' + ip + ' ' + port + '\n'
        # Creating a connection script
        file = open('connect.sh', 'w')
        file.write(conn_scpt)
        file.close()
        os.system("chmod +x connect.sh")

    # Creating a get flag script
    file = open('get_flag.sh', 'w')
    file.write('#!/bin/sh\n')
    file.close()
    os.system("chmod +x get_flag.sh")

    # Creating A readme script
    file = open('README.md', 'w')
    file.write(Readme)
    file.close()

    download(files)

    # Return to base directory
    os.chdir(base_dir)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("-n", "--name", help="Takes the name of the challenge")
    parser.add_argument("-d", "--desc", help="Add a Challenge  description")
    parser.add_argument("-c", "--conn", help="Netcat connection information")
    parser.add_argument("-f", "--files", help="wget remote files to download")
    parser.add_argument("-y", "--category", help="Category of the challenge")
    parser.add_argument("-p", "--points", help="Challenge Points")
    parser.add_argument("-l", "--links", help="link(s) to xyz ")
    parser.add_argument("-t", "--tags", help="Tags for the challenges")

    args = parser.parse_args()

    if args.name:
        name = args.name
    else:
        print("Name of challenge is required")
        exit(1)

    if args.desc:
        desc = args.desc
        urls = urlDetect(desc)
        if urls:
            for url in urls:
                if args.links:
                    if url not in args.links:
                        args.link += ',' + url
                else:
                    args.link = url

    if args.conn:
        connections = args.conn.split(',')
        conn = []
        for connection in connections:
            conn.append(
                connection.strip(' ').replace('nc', '').replace(':', ' ').split(' '))
    else:
        conn = ''
    if args.files:
        files = args.files.split(',')
    else:
        files = []
    if args.category:
        category = args.category
    else:
        category = ''
    if args.points:
        points = args.points
    else:
        points = ''
    if args.links:
        links = sanitise(args.links)
    else:
        links = ''
    if args.tags:
        tags = sanitise(args.tags)
    else:
        tags = ''

    Readme = genWriteup(name, conn, files, desc, category, points, links, tags)
    prepare(name, Readme, category, files, conn)
