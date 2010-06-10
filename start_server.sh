#!/bin/sh

# Where to find our own modules
export PYTHONPATH=/home/psirp/psirp

echo "Removing OS X crappy files"
rm -vf public/websocket/._*

echo "Initializing seats (fixme: this should not be needed, read Subscriber#listen())"
python2.6 _initialize_web_publishments.py

echo "Starting server"
cd mod_pywebsocket && \
python2.6 standalone.py -p 80 -d ../public -x /cgi --log-level=debug -m websocket/handler_map.txt -w websocket --allow-draft75 
