
var Subscriber = function(wsAddress, messageElementId, sid, rid, subscriberDomId) {

  if (!("WebSocket" in window)) {
    alert("Your browser does not support websockets.");
    return;
  };
  
  this.ws = new WebSocket(wsAddress);
  this.sid = sid;
  this.rid = rid;
  this.messageElementId = messageElementId;
  this.subscriberDomId = subscriberDomId;
  
  this.ws.onopen = function() {
    debug("connected...");
    this.send(sid +","+ rid); // HACK: comma separated: sid,rid (todo: json)
    this.send("more from browser");
  };

  this.ws.onmessage = function (event) {
    $("#"+messageElementId).append("<p>" + event.data + "</p>");
  };

  this.ws.onclose = function() {
    debug(" socket closed");
  };

  function debug(str){
    $("#debug").append("<p>" +  str);
  };

  this.sendButtonEvent = function(value) {
    this.ws.send("Nappia painettiin! Napin arvo: "+ value);
  };
  
}
