from publishment import *

Publishment('{"status": "SEAT_AVAILABLE"}', "::aa","::a1")
Publishment('{"status": "SEAT_AVAILABLE"}', "::aa","::a2")
Publishment('{"status": "SEAT_AVAILABLE"}', "::aa","::a3")
Publishment('{"status": "SEAT_AVAILABLE"}', "::aa","::a4")
Publishment('{"status": "SEAT_AVAILABLE"}', "::aa","::a5")
Publishment('{"status": "SEAT_AVAILABLE"}', "::aa","::a6")
Publishment('{"message": ""}', "::aa","::bb")

Publishment(open('public/images/reserve.png', 'rt').read(),"::aa","::c1")
Publishment(open('public/images/reserved.png', 'rt').read(),"::aa","::c2")
Publishment(open('public/images/my_reservation.png', 'rt').read(),"::aa","::c3")