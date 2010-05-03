#!/usr/bin/env python2.6

from publishment import *
from subscriber import *

def print_subscribers(msg):
	print msg
	loop_index = 1
	for s in [s1, s2]:
		print "\nSubscriber", loop_index
		print s
		loop_index = loop_index+1
	print "\n"


# Two subscribers subscribe to content before it is published
# ERROR: "psirp.libpsirp.ScopeNotFoundError: [Errno 3] Scope not found"

sid_1 = "::aa"
rid_1 = "::bb"

pub = Publishment("Test content for publishment")
pub.publish(sid_1, rid_1)

s1 = Subscriber(sid_1, rid_1)
s2 = Subscriber(sid_1, rid_1)

print_subscribers("Two subscribers subscribed to content before it is published.")


print "Publisher updates content."
pub.update_content("New content!")
s1.content.resubscribe
print_subscribers("Subscribers with new content.")


print "Publisment's buffer: ", pub.content.buffer


