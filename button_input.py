import uasyncio as asyncio
from machine import Pin
import time

class ButtonInput:
    def __init__(self, pin_number, callback=None, debounce_time_ms=150, button_name="button"):
        self.pin = Pin(pin_number, Pin.IN, Pin.PULL_UP)
        self.callback = callback
        self.debounce_time_ms = debounce_time_ms
        self.button_name = button_name
        self.last_press_time = 0
        self.pending_press = False

        # Attach interrupt
        self.pin.irq(trigger=Pin.IRQ_FALLING, handler=self._irq_handler)

    def _irq_handler(self, pin):
        """Minimal work in IRQ: just note that a press happened."""
        current_time = time.ticks_ms()
        if time.ticks_diff(current_time, self.last_press_time) > self.debounce_time_ms:
            self.last_press_time = current_time
            self.pending_press = True  # Flag for main loop

    def poll(self):
        """Call this periodically from main loop."""
        if self.pending_press:
            self.pending_press = False
            if self.callback:
                self.callback(self.button_name)


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
  b1 = ButtonInput(callback=button_callback, button_name="test_button", pin_number=15)

  # Keep the script running to allow event handling
  import time
  while True:
      time.sleep(0.05)
      b1.poll()
