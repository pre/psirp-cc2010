

window.onload = function() {
  
  $('.seat').each(function() {
    this.rid = "::"+ this.id;
    this.seat = new Seat(sid, this.rid, this.id, reserver);

    
    $(this).append('<img class="reservation click" src="images/reserve.png">');
    $(this).append('<img class="reserved" src="images/reserved.png">');
    $(this).append('<img class="confirmed" src="images/my_reservation.png">');
    $(this).append(
       "<ul class='reservation-details'>"
      +  "<li class='reserved-by'>Peke Vaara</li>"
      +  "<li class='reserved-at easydate'>Wed, 09 Jun 2010 06:42:23 -0700</li>"
      + "</ul>");
    $(this).append('<button class="cancel click">Cancel reservation</button>');

  });
  
  $('img.reservation, img.confirmed, img.reserved').hide();
  reserver.markReservations();
  
  $('.seat img.reservation').live('click', function() {
    $(this).parent()[0].seat.reserve();
  });
  
  $('.seat button.cancel').live('click', function() {
    $(this).parent()[0].seat.cancel();
  });
  
  messageSubscriber = new Subscriber(wsAddress, messageElementId, sid, "::bb");

}
function debug(str) {
  $("#debug").append(str + "<br />");
};



var Reserver = function() {
  
  this.name = function() {
    return $('#username').val();
  }

  this.announcePresence = function() {
    if (this.name() == "") {
      alert("Fill in your name first.");
      return;
    }
    messageSubscriber.sendMessage(this.name() + " has come to get some seats!");
  }  
  
  this.markReservations = function() {
    $('.seat').each(function() {
      reserver.markReservation(this);
    });
  };
  
  this.markReservation = function(seatElement) {
    $(seatElement).each(function() {
      if (this.seat.reserverName() == reserver.name()) {
        this.seat.confirm();
      }      
    });
  }
  
}

var Seat = function(sid, rid, domId, reserver) {
  this.domId = domId;
  this.sid = sid;
  this.rid = rid;
  this.reserver = reserver;
  this.subscriber = new Subscriber(wsAddress, messageElementId, this.sid, this.rid, this);

  this.reserve = function() {
    if (this.reserver.name() == "") {
      alert("Fill in your name first.");
      return;
    }
    this.subscriber.sendRequest("SEAT_RESERVATION", this.reserver.name());
    $("#"+this.domId).addClass("unconfirmed");
  };
  
  this.reserverName = function() {
    return $("#"+this.domId +" .reserved-by").html();
  }
  
  this.confirm = function() {
    $("#"+this.domId).removeClass("unconfirmed");
    $("#"+this.domId).removeClass("unavailable");
    $("#"+this.domId).addClass("confirmed");
    $("#"+this.domId+" img.confirmed").show();
    $("#"+this.domId+" img.reservation").hide();
    $("#"+this.domId+" img.reserved").hide();
  };
  
  /* NB. Since all application logic is in JavaScript, it is easily bypassed.
   *     Of course you can manually call cancel() function and bypass "security",
   *     but that is not the point here.
   *
   *     Now we depend on the caller to check that I am allowed to call this method.
   */
  this.cancel = function() {
    this.subscriber.sendRequest("SEAT_CANCELLATION");
    $("#"+this.domId).removeClass("unavailable");
    $("#"+this.domId).addClass("available");
    $("#"+this.domId+" ul.reservation-details").hide();
    
  }
  
  this.make_unavailable = function(reservedBy, reservedAt) {
    $("#"+this.domId).removeClass("available");
    $("#"+this.domId).addClass("unavailable");
    $("#"+this.domId+" button.cancel").show();
    $("#"+this.domId+" img.reservation").hide();
    $("#"+this.domId+" img.confirmed").hide();
    $("#"+this.domId+" img.reserved").show();
    $("#"+this.domId+" ul.reservation-details").show();
    $("#"+this.domId+" li.reserved-by").html(reservedBy);
    $("#"+this.domId+" li.reserved-at").html(reservedAt);
    reserver.markReservation("#"+this.domId);
  };

  this.make_available = function() {
    $("#"+this.domId).removeClass("unavailable");
    $("#"+this.domId).addClass("available");
    $("#"+this.domId+" button.cancel").hide();
    $("#"+this.domId+" img.reservation").show();
    $("#"+this.domId+" img.reserved").hide();
    $("#"+this.domId+" img.confirmed").hide();
    $("#"+this.domId+" ul.reservation-details").hide();
  };
  
}