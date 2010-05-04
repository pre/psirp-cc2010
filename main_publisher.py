#!/usr/bin/env python2.6

from psirp.libpsirp import *
from psirp import libpsirp
from publishment import *
from buffered_publishment import *

sid_1 = "::aa"
rid_1 = "::bb"

#p1 = Publisher(sid_1, rid_1)

p = Publishment("_OLD_CONTENT_OLD_CONTENT_OLD_CONTENT_OLD_CONTENT_OLD_CONTENT")
p.publish("::aa","::bb")
p.update_content("_new_content_new_content")


bp = BufferedPublishment("_OLD_BUFFERED_CONTENT_OLD_BUFFERED_CONTENT_OLD_BUFFERED_CONTENT")
bp.publish("::aa","::bb")
bp.update_content("_new_buffered_content_new_buffered_content")
