#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from stuinfo import app

if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run(host='0.0.0.0', port=8000)
