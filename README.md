This project is an RFID-based attendance tracker that reads RFID cards using the MFRC522 module, logs the UID to Firebase Realtime Database, and provides a web interface to display attendance logs and assign names to RFID cards.

Features
RFID Card Reading: Uses MFRC522 to scan RFID cards and log UIDs.
Firebase Integration: Logs data to Firebase Realtime Database, including timestamps and names.
Web Interface: Allows assigning names to UIDs and displays attendance logs via a Microdot-powered web server.
LED Feedback: LED turns on for successful RFID card read.

LIBRARIES:
I was having problems with libraries for the mfrc522 library but i was using these two libraries:
  https://github.com/wendlers/micropython-mfrc522
  https://github.com/Tasm-Devil/micropython-mfrc522-esp32

I was using microdot for the web framework, it worked well
  https://github.com/miguelgrinberg/microdot


I was using PyMakr(a micropython vs code web extension), but use whatever works for you...
