
var Subscriber = function(wsAddress, contentElementId, sid, rid) {

  if (!("WebSocket" in window)) {
    alert("Your browser does not support websockets.");
    return;
  }
  
  this.ws = new WebSocket(wsAddress);

  this.ws.onopen = function() {
    debug("connected...");
    this.send(sid +","+ rid); // HACK: comma separated: sid,rid (todo: json)
    this.send("more from browser");     // not handled yet
  };

  this.ws.onmessage = function (event) {
    // var data = evt.data;
    // var i = data.indexOf("!");
    // var tag = data.slice(0,i);
    // var val = data.slice(i+1);
    $(contentElementId).append("<p>" + event.data + "</p>");
  };

  this.ws.onclose = function() {
    debug(" socket closed");
  };

  function debug(str){
    $("#debug").append("<p>" +  str);
  };

  this.sendButtonEvent = function(value) {
    this.ws.send("Nappia painettiin! Napin arvo: "+ value);
  }
  
  this.testi = function() {
    alert("toimii");
  }

}
