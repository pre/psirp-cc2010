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
                        "cancel" : "SEAT_CANCELLATION"
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
        continue
      except ValueError, e:
        msg = json_message("message", "data is not json: "+ line)
        msgutil.send_message(self.websocket, '%s' % msg)


  # Note: Responses are not checked. We only assume that everything is ok.
  # PS Message parsing should be done in a more clever way... :P
  def act_on(self, msg):
    if msg.get("request") == self.messages['request']['reserve']:
      self.reserve()
    if msg.get("request") == self.messages['request']['cancel']:
      self.cancel()
    elif msg.get("message") is not None:
      msg = json_message("message", msg.get("message"))
      print "Publishing message: %s" % msg
      p = Publishment(msg, self.sid, self.rid)  
    else:
      print "Publishing (not matched with commands) %s" % str(msg)
      

  def reserve(self):
    self.publish_status('unavailable')
    self.send_status('confirmed')

    
  def cancel(self):
    self.publish_status('available')
    self.send_status('available')

    
  def publish_status(self, status):
    """Publish status to Blackhawk"""
    print("Publishing status: %s" %  json_message("status", self.messages['status'][status]))
    p = Publishment(json_message("status", self.messages['status'][status]))
    p.publish(self.sid, self.rid)

  def send_status(self, status):
    """Send status to websocket"""
    msgutil.send_message(self.websocket, '%s' % json_message("status", self.messages['status'][status]))
    
    
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
    for version in subscriber.listen():
      if version is not None: # if publication exists
        print('Sending: %s' % version.buffer)
        msgutil.send_message(request, '%s' % str(version.buffer))
      else:
        print("Received Publishment was null :(")


def web_socket_transfer_data(request):
  subscriber = initialize_subscriber(request)
  initial_content = subscriber.get_initial_content()  
  if initial_content is not None:
    print("Sending initial content: %s" % str(initial_content.buffer))
    msgutil.send_message(request, '%s' % str(initial_content.buffer))
  
  seat_reserver = SeatReserver(request, subscriber.sid, subscriber.rid)
  seat_reserver.start()

  listen_psirp_updates(request, subscriber)
