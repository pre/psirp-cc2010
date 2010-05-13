from mod_pywebsocket import msgutil
from subscriber import *
from publishment import *

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
        
      static_msg = json_message("message", str(line))
      p = Publishment(static_msg)
      p.publish(self.sid, self.rid)
###      msgutil.send_message(self.websocket, '%s' % static_msg)

  # Note: Responses are not checked. We only assume that everything is ok. This is only experimental stuff.
  # PS This should be done in a more clever way... :P
  def act_on(self, msg):
    if msg.get("request") == self.messages['request']['reserve']:
      self.reserve() 
      msgutil.send_message(self.websocket, '%s' % json_message("response", self.messages['status']['confirmed']))
    

  
  def reserve(self):
    print "reserving", self.rid
    p = Publishment(json_message("status", self.messages['status']['unavailable']))
    p.publish(self.sid, self.rid)
    
def json_message(msg_type, message):
  return json.dumps({msg_type : message})
   
def web_socket_do_extra_handshake(request):
  print "Connected."
  pass  # Always accept.

# First message must be a PSIRP subscription request:
#    subscribe : { sid : "::aa"
#                  rid : "::bb"
#                } 

def initialize_subscriber(request):
  line = msgutil.receive_message(request).encode('utf-8')
  try:
    msg = json.loads(line)
    sid = str(msg["subscribe"]["sid"])
    rid = str(msg["subscribe"]["rid"])
  except ValueError, e:
    msgutil.send_message(request, '%s' % json_message("message", str(e) + " " + line))
    return False
  msgutil.send_message(request, '%s' % json_message("message", "subscribing to sid: '"+sid+"', rid: '"+ rid +"'"))
  return Subscriber(sid, rid)

def listen_psirp_updates(request, subscriber):
  while True:
    for event in subscriber.listen():
      if event is not None:
        for version in event:
          print('Sending: %s' % version.buffer)
          msgutil.send_message(request, '%s' % str(version.buffer))


def web_socket_transfer_data(request):
  subscriber = initialize_subscriber(request)
  initial_content = subscriber.get_initial_content()  
  if initial_content is not None:
    msgutil.send_message(request, '%s' % json_message("message", 'Initial content: ' + str(initial_content.buffer)))
  
  seat_reserver = SeatReserver(request, subscriber.sid, subscriber.rid)
  seat_reserver.start()

  listen_psirp_updates(request, subscriber)
