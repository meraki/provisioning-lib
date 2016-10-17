call("+1" + number, {
   "network":"SMS"})
say("Guest WiFi password is: " + pw + "\nSent to guest: " + number);
log("Log for guest wifi pw send event");
