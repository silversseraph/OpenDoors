# OpenDoors
Access Control System for buildings based on raspberry pi
This is a simple project that creates a simple access control system on a raspberry pi.
Supports Wiegand readers connected to GPIO pins with an eventual logic level shifter in between to not damage the Pi GPIO's.
The successful car read if recognised will trigger a GPIO to activate a relay and release the lock opening the door.


pywiegand
RPi.GPIO
flask
flask_socketio
requests
