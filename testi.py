#!/usr/bin/env python2.6

from psirp.libpsirp import *


### Create first version

print "Create first version"
p = create(11)
p.buffer[:] = "1st version"
p.pub_s("::aa","::bb")

q = sub_s("::aa", "::bb")  

print "p buffer: ", p.buffer
print "q buffer: ", q.buffer

print "p version_count: ", p.version_count
print "p version_index: ", p.version_index
print "-"
print "q version_count: ", q.version_count
print "q version_index: ", q.version_index

print "---------"

print "Create new version"
p2 = create(11)
p2.buffer[:] = "2nd version"
p2.pub_s("::aa","::bb")

q2 = sub_s("::aa", "::bb")

print "p buffer: ", p.buffer
print "p2 buffer: ", p2.buffer

print "q buffer: ", q.buffer
print "q2 buffer: ", q2.buffer

print "p version_count: ", p.version_count
print "p version_index: ", p.version_index
print "p2 version_count: ", p2.version_count
print "p2 version_index: ", p2.version_index

print "-"
print "q version_count: ", q.version_count
print "q version_index: ", q.version_index
print "q2 version_count: ", q2.version_count
print "q2 version_index: ", q2.version_index
