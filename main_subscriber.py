#!/usr/bin/env python2.6

from publishment import *
from subscriber import *

sid_1 = "::aa"
rid_1 = "::bb"

s1 = Subscriber(sid_1, rid_1)

print "Before resubscribe():"
print s1

print "Initial content:"
ic = s1.get_initial_content()
print ic.buffer

print "\nListening for updates:"
for event in s1.listen():
  if event is not None:
    for version in event:
      print "Received: ", version.buffer

print s1



