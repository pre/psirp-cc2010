
var Subscriber = function(wsAddress, messageElementId, sid, rid, caller) {

  if (!("WebSocket" in window)) {
    debug("Your browser does not support websockets.");
    return;
  };
  
  this.ws = new WebSocket(wsAddress);
  this.sid = sid;
  this.rid = rid;
  this.messageElementId = messageElementId;
  
  this.ws.onopen = function() {
    // How to build json with a generator?
    subscriptionRequest = '{ "subscribe": { \
                                "sid" : "' + sid + '", \
                                "rid" : "' + rid + '" \
                             } \
                            }';
    this.send(subscriptionRequest);
    debug("connected: "+ rid);
  };

  this.ws.onmessage = function (event) {
    this.parseResponse(event.data);
  };

  this.ws.onclose = function() {
    debug("disconnected: "+ rid);
  };

  this.sendButtonEvent = function(value) {
    msg = '{ "message" : "Button was clicked! Its value: '+ value +'" }'
    this.ws.send(msg);
  };
  
  this.ws.parseResponse = function(data) {
    var json_data = null;
    try {
      json_data = jQuery.parseJSON(data);
    } catch(err) {
      debug("Error parsing response: " + err);
      return;
    };
    
    if ( json_data.response == "SEAT_CONFIRMED" ) {
      caller.confirm();
    }
    if ( json_data.status == "SEAT_UNAVAILABLE" ) {
      caller.make_unavailable();
    }
    if ( json_data.status == "SEAT_AVAILABLE" ) {
      caller.make_available();
    }
    if ( json_data.message != undefined ) {
      this.display_message(json_data.message);
    }
    
    //debug("Unknown response: " + json_data) // FIXME: Howto print json_data contents?

  };
  
  this.ws.display_message = function(msg) {
    $("#"+messageElementId).append(msg + "<br />");
  };
  
  this.request = function(msg) {
    msg = '{ "request": "'+ msg +'" }'
    this.ws.send(msg);
  };
  
}