from psirp.libpsirp import *

class Subscriber(object):
	
	def __init__(self, sid, rid):
		self.content = sub_s(sid, rid)
		self.sid = sid
		self.rid = rid
		
		
	def content(self):
		return self.content

	def __str__(self):
		return "* content:       "+ str(self.content.buffer)+ "\n* version index: "+ str(self.content.version_index)+ "\n* version count: "+ str(self.content.version_count)
		
		