from psirp.libpsirp import *

MAX_PRINT_LEN = 100 # This is just for testing

def exc_handler(exception):
    """Exception handler function."""
    from traceback import print_exc
    print_exc() # Just print what happened and try to proceed


def handle_event(event, pub):
    """Event handler function."""
    
    # First we could check that the event is NOTE_PUBLISH (the default
    # for publication updates). In our example it can also be None, so
    # we just ignore this check.
    
    # Process all versions since the last seen one. When a publication
    # is subscribed to, the saved_version_index variable is initially
    # the subscribed version's index minus 1. The saved index is then
    # updated to the current index of pub in the call below.
    for version in pub.get_versions_since_saved_index():
        # Here we do whatever we want to do with the version
        print("First %d bytes of version %s of %s:\n%s\n"
              % (MAX_PRINT_LEN, version.vridstr, idstoa(pub.sid, pub.rid),
                 version.buffer[:MAX_PRINT_LEN]))

def get_init_handle_event(pskq):
    """Getter for the initial event handler."""
    
    # This nesting allows us to use the outer function's variables
    # (e.g., pskq or self) in the inner function.
    
    def init_handle_event(event, pub):
        """Initial event handler function."""
        
        # Register to future events
        pskq.register(pub, False)
        
        # Here we could resubscribe (locally) to the publication in order
        # not to miss any versions that might have appeared just before
        # event registration. But this time we just skip that and trust
        # that everything goes fine anyway.
        
        # Set the "normal" event handler
        pub.handle_event = handle_event
        
        # Call event handler. We could leave out this call, or do
        # something else at this point if needed. Moreover, we could
        # change the publication's saved_version_index first, e.g. if
        # we want to process all versions starting from 0 (in which
        # case we would set the saved index to -1). Or if we skip the
        # existing version, we'd need to set it to the current index.
        pub.handle_event(event, pub)
        
        # Re-register and request automatic publication updating
        pskq.register(pub, True)
        # At this point, pub has become unmapped! The object still
        # exists, but its buffer, length information, or identifiers
        # can no longer be accessed. Their content must not be
        # referred to, either. Any data that needs to persist must be
        # copied before the unmapping takes place (i.e., before
        # calling register() or listen()). Otherwise, segmentation
        # faults will occur.
    
    return init_handle_event


pskq = PubSubKQueue()
init_handle_event = get_init_handle_event(pskq)
sid = atoid("::aa")
rid = atoid("::bb")
asd = pskq.register_advance_subscription(sid, rid, PS_FLAGS_LOCAL_NETSUB|PS_FLAGS_NET_PERSISTENT, init_handle_event)

if isinstance(asd, Publication):
    print "inside!"
    print "no?"
    # In this case the publication already exists - as an
    # example, we here call the initial event handler.
    pub = asd # This adv. sub. descriptor is really a publication
    init_handle_event(None, pub)

def exc_handler(exception):
    """Exception handler function."""
    from traceback import print_exc
    print_exc() # Just print what happened and try to proceed

print("Listen to events")
try:
    pskq.listen_and_handle(exc_handler) # Event handling "loop"
except KeyboardInterrupt:
    # E.g. ^C pressed
    print("Interrupted")
    
print "test"

#def _main():
# Some SId/RId pairs
# sid_rids = ((atoid("::aa"), atoid("::bb")),
#             (atoid("88::77"), atoid("ee::dd")),
#             (atoid("88::77"), atoid("dd::cc")))
# 
# # Subscription flags; these are useful for "network subscriptions"
# sub_flags = PS_FLAGS_LOCAL_NETSUB|PS_FLAGS_NET_PERSISTENT
# 
# # Open an event queue
# pskq = PubSubKQueue()
# 
# # Subscribe to the defined publications
# for sid, rid in sid_rids:
#     print("Subscribing to SId/RId: %s" % idstoa(sid, rid))
#     
#     init_handle_event = get_init_handle_event(pskq)
#     
#     # Try to register to a publication that maybe doesn't exist
#     # yet. By using only one queue, we can avoid doing synchronous
#     # subscriptions in multiple parallel threads. That ought to
#     # simplifiy our code quite significantly.
#     asd = pskq.register_advance_subscription(sid, rid, sub_flags,
#                                              init_handle_event)
#     
#     if isinstance(asd, Publication):
#         # In this case the publication already exists - as an
#         # example, we here call the initial event handler.
#         pub = asd # This adv. sub. descriptor is really a publication
#         init_handle_event(None, pub)
# 
# def exc_handler(exception):
#     """Exception handler function."""
#     from traceback import print_exc
#     print_exc() # Just print what happened and try to proceed
# 
# print("Listen to events")
# try:
#     pskq.listen_and_handle(exc_handler) # Event handling "loop"
# except KeyboardInterrupt:
#     # E.g. ^C pressed
#     print("Interrupted")
# 
# # Close the event queue (although it gets closed anyway at exit time)
# pskq.close()
