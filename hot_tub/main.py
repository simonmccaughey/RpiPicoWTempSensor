import machine
import time

# Define GPIO pins
RELAY_1_PIN = 14  # Change to your actual GPIO pin
RELAY_2_PIN = 15  # Change to your actual GPIO pin

print("Initializing relays")

# Initialize relays
relay1 = machine.Pin(RELAY_1_PIN, machine.Pin.OUT)
relay2 = machine.Pin(RELAY_2_PIN, machine.Pin.OUT)

# Turn both relays ON initially
print("Turning on relays")
relay1.value(1)
#small delay before starting the heater
time.sleep(3)
relay2.value(1)

while True:
    #time.sleep(10)  # Wait for 19 minutes
    time.sleep(19 * 60)  # Wait for 19 minutes
    print('Turning off relay 2')
    relay2.value(0)  # Turn off relay 2
    time.sleep(30)  # Keep it off for 1 minute
    # time.sleep(1)  # Keep it off for 1 minute
    print('Turning on relay 2')
    relay2.value(1)  # Turn relay 2 back on
