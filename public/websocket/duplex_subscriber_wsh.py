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
      print("received %s" % line)
      msgutil.send_message(self.websocket, 'vastaanotettu: %s' % line)


def web_socket_do_extra_handshake(request):
  print "Connected."
  pass  # Always accept.

def web_socket_transfer_data(request):
  print "Transfer"
  sid, rid = msgutil.receive_message(request).encode('utf-8').split(",")  # TODO: JSON
  print "sid: "+ sid + " rid: " + rid
  msgutil.send_message(request, "subscribing to sid: '"+sid+"', rid: '"+ rid +"'")
  sub = Subscriber(sid, rid)
  
  duplex = duplex_subscriber(request)
  duplex.start()
  
  initial_content = sub.get_initial_content()
  print "Sending initial content: ", initial_content.buffer
  msgutil.send_message(request, 'Initial content: %s' % initial_content.buffer)
  while True:
    for event in sub.listen():
      if event is not None:
        for version in event:
          print('Sending: %s' % version.buffer)
          msgutil.send_message(request, '%s' % version.buffer)
