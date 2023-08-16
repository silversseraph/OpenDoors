import time
import RPi.GPIO as GPIO
from  pywiegand import WiegandReader

# Card reader Data0 on GPIO 6, Data1 on GPIO 5
wr = WiegandReader(6, 5)

# Relay on GPIO 25
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT, initial=GPIO.HIGH)

# Read for 10 to 20 secondes
# When card is readed, the replay will be trigged
print("Use the access card 3 times withing 1.5 second interval")
totalPass = 3
while totalPass:
	# Check each 1 second
	time.sleep(1)
	card = wr.read()
	if (card):
		totalPass -= 1
		print(f"Card ID: {card}")
		# Activate the relay for 3 seconds
		GPIO.output(26, GPIO.LOW)
		print("Door Unlocked")
		for i in range (3):
			print(3-i)
			time.sleep(1)
		# Deactivate the relay
		GPIO.output(26, GPIO.HIGH)
		print("Door Locked")

# Free used resources
GPIO.cleanup(26)

