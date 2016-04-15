#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import argv
from stuinfo.db import create_table


if __name__ == '__main__':
    drop = len(argv) > 1 and argv[1] == '--drop'
    print('drop:', drop)
    create_table(drop)
