
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
    alert("TODO DONT BUILD JSON BY HAND :/")
    subscriptionRequest = '{"subscribe": 
                             {
                              "sid" : +sid XXX
                              "rid" : +rid XXX
                             }
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
    this.ws.send("Nappia painettiin! Napin arvo: "+ value);
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
