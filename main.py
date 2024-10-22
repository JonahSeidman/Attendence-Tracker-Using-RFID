import urequests
from machine import Pin, SPI
from mfrc522 import MFRC522
import time
import json

# Replace with your network credentials
ssid = "xxx" #wifi name
password = "xxx" #wifi pw

# Firebase project details
FIREBASE_API_KEY = "xxx" #firebae api key
FIREBASE_DATABASE_URL = "xxx/" #firebase database URL(remember to add a / at the end)

# RFID and LED setup
SS_PIN = 21   # RFID SS pin
RST_PIN = 22  # RFID reset pin
SCK_PIN = 18  # SPI clock
MOSI_PIN = 23 # SPI MOSI
MISO_PIN = 19 # SPI MISO
LED_PIN = 13  # LED pin for lighting up

# Setup SPI and MFRC522 RFID reader
spi = SPI(1, baudrate=1000000, polarity=0, phase=0, sck=Pin(SCK_PIN), mosi=Pin(MOSI_PIN), miso=Pin(MISO_PIN))
rdr = MFRC522(spi, Pin(SS_PIN))

# Setup LED
led = Pin(LED_PIN, Pin.OUT)

# Function to check if the UID exists in Firebase
def check_rfid_exists(uid):
    url = f"{FIREBASE_DATABASE_URL}rfid_logs/{uid}.json?auth={FIREBASE_API_KEY}"
    try:
        response = urequests.get(url)
        return response.json() is not None  # Returns True if exists, False if new
    except Exception as e:
        print(f"Error checking UID in Firebase: {e}")
        return False

# Function to send RFID data to Firebase
def send_to_firebase(uid, timestamp, is_new):
    url = f"{FIREBASE_DATABASE_URL}rfid_logs/{uid}.json?auth={FIREBASE_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = json.dumps({"timestamp": timestamp, "is_new": is_new})
    try:
        response = urequests.put(url, data=data, headers=headers)
        print(f"Data sent to Firebase: {response.text}")
    except Exception as e:
        print(f"Failed to send data to Firebase: {e}")

# Main loop to handle RFID scanning
def main():
    while True:
        # Check for RFID card
        if rdr.request(rdr.REQIDL):
            (status, raw_uid) = rdr.anticoll()
            if status == rdr.OK:
                uid = "".join(f"{b:02x}" for b in raw_uid).upper()  # Convert UID to readable format
                print(f"Card UID: {uid}")
                timestamp = time.time()

                # Turn the LED on for 1 second after reading the card
                led.on()
                time.sleep(1)
                led.off()

                # Check if the UID exists in Firebase and send the data
                is_new = not check_rfid_exists(uid)
                send_to_firebase(uid, timestamp, is_new)
        time.sleep(1)

main()
