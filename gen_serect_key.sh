#!/bin/sh

RAND_KEY=`date +%s%N | md5sum | head -c 16`

echo "SECRET_KEY = '$RAND_KEY'" | tee -a ./stuinfo/config.py
