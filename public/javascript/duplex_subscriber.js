
var Subscriber = function(wsAddress, messageElementId, sid, rid) {

  if (!("WebSocket" in window)) {
    alert("Your browser does not support websockets.");
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
    debug(subscriptionRequest);
    this.send(subscriptionRequest);
    debug("connected: "+ rid);
  };

  this.ws.onmessage = function (event) {
    $("#"+messageElementId).append(event.data + "<br />");
    this.parseResponse(event.data);
  };

  this.ws.onclose = function() {
    debug("disconnected: "+ rid);
  };

  function debug(str){
    $("#debug").append(str + "<br />");
  };

  this.sendButtonEvent = function(value) {
    msg = '{ "message" : "Nappia painettiin! Napin arvo: '+ value +'" }'
    this.ws.send(msg);
  };
  
  this.ws.parseResponse = function(data) {
    try {
      response = jQuery.parseJSON(data);
      debug("TODO: handler code for response!")
    } catch(err) {
      debug("Error parsing response: " + err);
    };
  }
}
