from psirp.libpsirp import *

class Publisher(object):
	
	#		pub.pub_s("::aa","::bb")		
	def publish(self, publishment, sid, rid):
		self.publishment.pub_s(sid, rid)
	
