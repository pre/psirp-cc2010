from psirp.libpsirp import *
from event_behaviour import *

class Subscriber(object):
	
  def __init__(self, sid, rid):
    self.sid = atoid(sid)
    self.rid = atoid(rid)
    self.sub_flags = PS_FLAGS_LOCAL_NETSUB|PS_FLAGS_NET_PERSISTENT
    self.register_subscription()

  def register_subscription(self):
    self.pskq = PubSubKQueue()
    init_handle_event = get_init_handle_event(self.pskq)
    asd = self.pskq.register_advance_subscription(self.sid, 
                                                   self.rid, 
                                                   self.sub_flags, 
                                                   init_handle_event)


    print asd   
    
    if isinstance(asd, Publication):

      # In this case the publication already exists - as an
      # example, we here call the initial event handler.
      self.content = asd # This adv. sub. descriptor is really a publication
      init_handle_event(None, self.content)		
		
  def content(self):
    return self.content
  
  def listen(self):
    try:
        self.pskq.listen_and_handle(exc_handler) # Event handling "loop"
    except KeyboardInterrupt:
        # E.g. ^C pressed
        print("Interrupted")
          
  def __str__(self):
    return   "* content:       "+ str(self.content) #+ \
#           "\n* version index: "+ str(self.content.version_index) #+ \
#           "\n* version count: "+ str(self.content.version_count)
		
		
		
		
