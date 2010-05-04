from psirp.libpsirp import *

class Publishment(object):
	
	def __init__(self, content):
		self.content = create(len(content))
		self.content.buffer[:len(content)] = content

	def publish(self, sid, rid):
		self.content.pub_s(sid, rid)
		self.sid = sid
		self.rid = rid
		
	def update_content(self, new_content):
		new_pub = create(len(new_content))
		new_pub.buffer[:] = new_content
		self.content = new_pub
		self.content.pub_s(self.sid, self.rid)
			
	