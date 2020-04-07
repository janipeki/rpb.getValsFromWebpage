#!/bin/bash

cd /opt/getStats
while :; do wget -q https://www.worldometers.info/coronavirus/ -O Corona.html; python3 readRedis.py Corona.html; sleep 300; done
