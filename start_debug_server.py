#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from stuinfo import app

if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['SECRET_KEY'] = 'development key'
    app.run(host='0.0.0.0', port=8000)
