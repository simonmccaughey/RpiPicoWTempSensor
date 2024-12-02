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
        self.button_a = Pin(12, Pin.IN, Pin.PULL_UP)
        self.button_b = Pin(13, Pin.IN, Pin.PULL_UP)
        self.button_x = Pin(14, Pin.IN, Pin.PULL_UP)
        self.button_y = Pin(15, Pin.IN, Pin.PULL_UP)

        # Set up interrupts for button presses
        self.button_a.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin: self._handle_button("a"))
        self.button_b.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin: self._handle_button("b"))
        self.button_x.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin: self._handle_button("x"))
        self.button_y.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin: self._handle_button("y"))

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
            if self.callback:
                self.callback(button_id)

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
