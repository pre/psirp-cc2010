#!/usr/bin/env python2.6

from publishment import *
from buffered_publishment import *

from time import sleep
from subprocess import *

def system_uptime():
  return Popen(["uptime"], stdout=PIPE).communicate()[0]  
  
sid_1 = "::aa"
rid_1 = "::bb"
sleep_amount = 4

print "Publishing initial content.."
p = Publishment("_OLD_CONTENT_OLD_CONTENT_OLD_CONTENT_OLD_CONTENT_OLD_CONTENT")
p.publish(sid_1, rid_1)
sleep(sleep_amount)

print "Updating it.."
p.update_content("_new_content_new_content")
sleep(sleep_amount)

print "Publishing system uptime.."
p.update_content(system_uptime())
sleep(sleep_amount)

print "Publishing content with BufferedPublishment.."
bp = BufferedPublishment("_OLD_BUFFERED_CONTENT_OLD_BUFFERED_CONTENT_OLD_BUFFERED_CONTENT_OLD_BUFFERED_CONTENT_OLD_BUFFERED_CONTENT_OLD_BUFFERED_CONTENT")
bp.publish(sid_1, rid_1)
sleep(sleep_amount)

print "Replacing content with shorter string without cleaning up older content.."
bp.replace_content("_new_buffered_content_new_buffered_content")
bp.replace_content("Buffered: " + system_uptime())
