from machine import Pin
import time

class ButtonInput:
    def __init__(self, callback=None, debounce_time_ms=50):
        self.callback = callback
        self.debounce_time_ms = debounce_time_ms
        
        # Dictionary to store the last press time for each button
        self.last_press_time = {
            "a": 0,
            "b": 0,
            "x": 0,
            "y": 0
        }

        # Initialize pins for buttons
        self.buttons = {
            "a": Pin(12, Pin.IN, Pin.PULL_UP),
            "b": Pin(13, Pin.IN, Pin.PULL_UP),
            "x": Pin(14, Pin.IN, Pin.PULL_UP),
            "y": Pin(15, Pin.IN, Pin.PULL_UP)
        }

        # Set up interrupts for button presses
        for button_id, pin in self.buttons.items():
            pin.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin, btn=button_id: self._handle_button(btn))

    def _handle_button(self, button_id):
        """
        Internal method to handle button press events with debounce.
        Calls the provided callback with the button ID if it exists.
        """
        current_time = time.ticks_ms()
        last_time = self.last_press_time[button_id]

        # Check if the time since the last press is greater than the debounce time
        if time.ticks_diff(current_time, last_time) > self.debounce_time_ms:
            self.last_press_time[button_id] = current_time
            self._check_multiple_buttons()

    def _check_multiple_buttons(self):
        """
        Check the state of all buttons and detect multiple button presses.
        Calls the callback with a string of currently pressed buttons.
        """
        # Get a sorted list of pressed buttons
        pressed_buttons = sorted([btn for btn, pin in self.buttons.items() if not pin.value()])
        
        # Join the button IDs into a single string
        if pressed_buttons and self.callback:
            self.callback("".join(pressed_buttons))

# Example usage
def button_callback(pressed_buttons):
    print(f"Buttons pressed: {pressed_buttons}")

# Example usage
def button_callback(pressed_buttons):
    if len(pressed_buttons) == 1:
        print(f"Button {pressed_buttons[0]} pressed")
    else:
        print(f"Multiple buttons pressed: {', '.join(pressed_buttons)}")

# Example usage
def button_callback(button_id):
    print(f"Callback triggered by button: {button_id}")

if __name__ == "__main__":

  # Create the ButtonInput instance with the callback function
  print("getting ready to test button input")
  button_input = ButtonInput(callback=button_callback)

  # Keep the script running to allow event handling
  import time
  while True:
      time.sleep(0.1)
