from mod_pywebsocket import msgutil
from subscriber import *

from threading import Thread
import os
import re
import sys
import time

class duplex_subscriber(Thread):
  def __init__(self, websocket):
    Thread.__init__(self)
    self.websocket = websocket
    
  def run(self):
    while True:
      line = msgutil.receive_message(self.websocket).encode('utf-8')
      msgutil.send_message(self.websocket, 'vastaanotettu: %s' % line)


def web_socket_do_extra_handshake(request):
  print "Connected."
  pass  # Always accept.

def web_socket_transfer_data(request):
  print "Transfer"
  sid, rid = msgutil.receive_message(request).encode('utf-8').split(",")
  print "sid: "+ sid + " rid: " + rid
  msgutil.send_message(request, "subscribing to sid: '"+sid+"', rid: '"+ rid +"'")
  s1 = Subscriber(sid, rid)
  
  duplex = duplex_subscriber(request)
  duplex.start()
  while True:
    for event in s1.listen():
      if event is not None:
        for version in event:
          print('Sending: %s' % version.buffer)
          msgutil.send_message(request, '%s' % version.buffer)
