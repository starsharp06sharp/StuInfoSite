#!/bin/sh

python create_table.py

uwsgi uwsgi.ini
