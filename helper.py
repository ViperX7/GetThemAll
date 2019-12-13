#!/bin/python3
import argparse
import stat
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
        filename = link.split('?')[0]
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
    Readme += '> ' + str(category) + ' | ' + str(pts) + ' points\n'
    Readme += '--------------------' + '\n\n'
    if tags:
        for tag in tags:
            Readme += 'Link + ' + tag + '  '
        Readme += '\n\n'
    Readme += '## Problem Statement\n'
    Readme += '> ' + desc + '  \n'
    if nc:
        Readme += '> * Connect using: nc' + nc[0] + ' ' + nc[1] + '\n'
    if links:
        for link in links:
            Readme += '> * [*' + link + '*](' + link + ')\n'
    if files:
        for file in files:
            Readme += '> * [*' + file + '*](./' + file + ')\n'
    return Readme


def prepare(name, category='.', files='', conn=''):
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
        file = open('connect.sh', 'w')
        file.write(conn_scpt)
        file.close()
        os.system("chmod +x connect.sh")

    file = open('get_flag.sh', 'w')
    file.write('#!/bin/sh\n')
    file.close()
    os.system("chmod +x get_flag.sh")

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
        for url in urls:
            if url not in args.links:
                args.link += ',' + url

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

    prepare(name, category, files, conn)
