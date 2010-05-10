
var Subscriber = function(wsAddress, contentElementId, sid, rid) {

  this.ws = null;
  
  if ("WebSocket" in window) {
    debug("Trying to connect...");
    ws = new WebSocket(wsAddress);

    ws.onopen = function() {
      // Web Socket is connected. You can send data by send() method.
      debug("connected...");
      ws.send(sid +","+ rid); // comma separated: sid,rid (todo: json)
      ws.send("more from browser");     // not handled yet
    };

    ws.onmessage = function (event) {
      // var data = evt.data;
      // var i = data.indexOf("!");
      // var tag = data.slice(0,i);
      // var val = data.slice(i+1);
      $(contentElementId).append("<p>" + event.data + "</p>");
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
