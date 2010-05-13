from mod_pywebsocket import msgutil
from subscriber import *

from threading import Thread
import os
import re
import sys
import time
import json

class SeatReserver(Thread):
  def __init__(self, websocket, sid, rid):
    Thread.__init__(self)
    self.websocket = websocket
    self.sid = sid
    self.rid = rid
    self.messages = {"request": {
                        "reserve": "SEAT_RESERVATION",
                        "cancel" : "SEAT_CANCEL"
                      },
                     "status": {
                         "unavailable" : "SEAT_UNAVAILABLE",
                         "confirmed"   : "SEAT_CONFIRMED",
                         "available"   : "SEAT_AVAILABLE"
                      }
                    }

  def run(self):
    while True:
      line = msgutil.receive_message(self.websocket).encode('utf-8')
      print("received %s" % line)
      try:
        msg = json.loads(line)
        self.act_on(msg)
      except ValueError, e:
        msg = json_message("message", "data is not json: "+ line)
        msgutil.send_message(self.websocket, '%s' % msg)
      msgutil.send_message(self.websocket, '%s' % json_message("message", 'received: ' + str(line)))

  # Note: Responses are not checked. We only assume that everything is ok. This is only experimental stuff.
  # PS This should be done in a more clever way... :P
  def act_on(self, msg):
    if msg.get("request") == self.messages['request']['reserve']:
      self.reserve(self.rid) 
      msgutil.send_message(self.websocket, '%s' % json_message("response", self.messages['status']['confirmed']))
    

  
  def reserve(self, rid):
    print "reserving", rid
    pass
    
def json_message(type, message):
  return json.dumps({type : message})
   
def web_socket_do_extra_handshake(request):
  print "Connected."
  pass  # Always accept.

# First message must be PSIRP subscription request:
#    subscribe : { sid : "::aa"
#                  rid : "::bb"
#                } 
def web_socket_transfer_data(request):
  line = msgutil.receive_message(request).encode('utf-8')
  print line
  try:
    msg = json.loads(line)
    sid = str(msg["subscribe"]["sid"])
    rid = str(msg["subscribe"]["rid"])
  except ValueError, e:
    response = json_message("message", str(e) + " " + line)
    msgutil.send_message(request, '%s' % response)
    return False
    
  print "sid: "+ sid + " rid: " + rid
  msgutil.send_message(request, '%s' % json_message("message", "subscribing to sid: '"+sid+"', rid: '"+ rid +"'"))
  sub = Subscriber(sid, rid)
  
  initial_content = sub.get_initial_content()  
  if initial_content is not None:
    msgutil.send_message(request, '%s' % json_message("message", 'Initial content: ' + str(initial_content.buffer)))
  
  seat_reserver = SeatReserver(request, sid, rid)
  seat_reserver.start()
 
  while True:
    for event in sub.listen():
      if event is not None:
        for version in event:
          print('Sending: %s' % version.buffer)
          msgutil.send_message(request, '%s' % json_message("message", str(version.buffer)))
