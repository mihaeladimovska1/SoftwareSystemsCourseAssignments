#!usr/bin/env python3
# method for creating the index file for lisitng directories
import os


def create_index(root_dir):
    str1 = '<!DOCTYPE html>'
    str1 += '<html><head><title> \n Files: </title><style type="text/css">table.fileList { text-align: left; }td.directory { font-weight: bold; }td.file { padding-left: 4em; }</style></head>\n<body><h1>Files</h1><table class="fileList">\n'

    for dirpath, dirs, files in os.walk(root_dir):
        path = dirpath.split('/')
        str1 += ' <tr><td class="directory">'
        str1 += os.path.basename(dirpath)
        str1 += '</td></tr>\n'
        # print( '|', (len(path))*'---', '[', os.path.basename(dirpath),']')
        for f in files:
            str1 += '<tr><td>'
            str1 += '<a href="'
            if len(path) > 2:
                for i in range(2, len(path)):
                    str1 += path[i] + "/"
            str1 += f
            str1 += '">'
            str1 += len(path) * '---'
            str1 += f
            str1 += '</a>'
            str1 += '</td></tr>\n'

        # print( '|', len(path)*'---', '<a href= "file:///localhost/',f, '" </a>')
    str1 += '<form action="/cgi-bin/date.py" method="get"> <input type="submit" /> Get Date </form>'
    str1 += '</table></body></html>\n'

    with open(root_dir + "/index.html", "w") as text_file:
        text_file.write(str1)
