#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import argv, exit
from stuinfo import app
from stuinfo.db import create_table


if __name__ == '__main__':
    if len(argv) <= 1:
        print('Need db host')
        exit()
    app.config['MYSQL_HOST'] = argv[1]
    drop = len(argv) > 2 and argv[2] == '--drop'
    print('drop:', drop)
    with app.app_context():
        create_table(drop)
