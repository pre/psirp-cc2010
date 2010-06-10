
var Subscriber = function(wsAddress, contentElementId, sid, rid) {

  this.ws = null;
  
  if ("WebSocket" in window) {
    debug("Trying to connect...");
    ws = new WebSocket(wsAddress);

    ws.onopen = function() {
      debug("connected...");
      ws.send(sid +","+ rid); // comma separated: sid,rid
      ws.send("more from browser");
    };

    ws.onmessage = function (event) {
      $(contentElementId).append("<br />" + event.data);
    };

    ws.onclose = function() {
      debug(" socket closed");
    };
  } else {
      alert("You have no web sockets");
  };

  function debug(str){
    $("#debug").append("<p>" +  str);
  };
  
}
