from psirp.libpsirp import *
from event_behaviour import *

class Subscriber(object):
	
  def __init__(self, sid, rid):
    self.content = None
    self.sid = sid
    self.rid = rid
    # Subscribe only to new publishments
    self.sub_flags = PS_FLAGS_LOCAL_NETSUB|PS_FLAGS_LOCAL_FUTUREONLY
#    self.sub_flags = PS_FLAGS_LOCAL_NETSUB|PS_FLAGS_NET_PERSISTENT
    self.register_subscription()

  def register_subscription(self):
    self.pskq = PubSubKQueue()
    init_handle_event = get_init_handle_event(self.pskq)
    asd = self.pskq.register_advance_subscription(atoid(self.sid), 
                                                  atoid(self.rid), 
                                                  self.sub_flags, 
                                                  init_handle_event)
    if isinstance(asd, Publication):
      # In this case the publication already exists - as an
      # example, we here call the initial event handler.
      self.content = asd # This adv. sub. descriptor is really a publication
      init_handle_event(None, self.content)

  # Loop copied from PubSubKQueue#listen_and_handle()  
  # and modified to yield return value for output processing.
  #
  # FIXME: For some reason advance subscription does not work. 
  #        If publication does not exist when subscribing, the first publishment
  #        results in PubNotFoundError - and the subscriber won't get any content.
  def listen(self):
    try:
      while True:
        timeout = None
        max_tot_evs = None
        evpubl = self.pskq.listen(1, timeout)
        if len(evpubl) == 0:
          raise PubSubTimeoutException("Timeout")
        for ev, pub in evpubl:
          try:
            for version in pub.get_versions_since_saved_index():
              yield(version)
          except PubNotFoundError:
            yield(None)
#          except Exception, e:
#            exc_handler(e)

    except KeyboardInterrupt:
      # E.g. ^C pressed
      print("Interrupted")
  
  # Warning: You will get "Segmentation fault: 11" if trying to 
  # return sub_s(..).buffer
  # access get_initial_content().buffer.
  def get_initial_content(self):
    try:
      return sub_s(self.sid, self.rid)
    except ScopeNotFoundError, e:
      return None
    except PubNotFoundError, e:
      return None
    
  def __str__(self):
    val =  "Subscriber:" 
    if isinstance(self.content, Publication):
      val = val + \
           "\n* content:       "+ str(self.content.buffer) + \
            "\n* version index: "+ str(self.content.version_index) + \
            "\n* version count: "+ str(self.content.version_count)
    else:
      val = val + " empty"
    return val
