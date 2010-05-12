
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
    debug("connected: "+ rid);
    this.send(sid +","+ rid); // HACK: comma separated: sid,rid (todo: json)
    this.send("more from browser");
  };

  this.ws.onmessage = function (event) {
    $("#"+messageElementId).append(event.data + "<br />");
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
  
}
