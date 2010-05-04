#!/usr/bin/env python2.6

from publishment import *
from subscriber import *


sid_1 = "::aa"
rid_1 = "::bb"

s1 = Subscriber(sid_1, rid_1)

print s1

print "\nListening for updates:"
s1.listen()

print s1



