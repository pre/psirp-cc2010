#!/usr/bin/env python2.6

# A simple Web <-> Blackhawk gateway for static images.
#
# A request URI "/cgi/image.py?a1" is translated to
# RID="::a1" with a hardcoded SID (e.g. "::aa").
#
# Content is delivered with mime-type image/jpeg to the
# requesting web browser. Image must already have been 
# published to Blackhawk.

import os
from psirp.libpsirp import *

sid="::aa"
image_rid = "::"+ os.environ['QUERY_STRING']

if __name__ == "__main__":
  img_sub = sub_s(sid, image_rid)
  print "Content-type: image/png\n"
  print img_sub.buffer


