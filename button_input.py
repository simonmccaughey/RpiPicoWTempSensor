import uasyncio as asyncio
from machine import Pin
import time

class AsyncButton:
    def __init__(self, pin_number, callback=None, debounce_ms=100, button_name="button"):
        self.pin = Pin(pin_number, Pin.IN, Pin.PULL_UP)
        self.callback = callback
        self.debounce_ms = debounce_ms
        self.button_name = button_name
        self._last_press_time = 0
        self._flag = asyncio.ThreadSafeFlag()

        self.pin.irq(trigger=Pin.IRQ_FALLING, handler=self._irq_handler)
        asyncio.create_task(self._debounce_task())

    def _irq_handler(self, pin):
        now = time.ticks_ms()
        if time.ticks_diff(now, self._last_press_time) > self.debounce_ms:
            self._last_press_time = now
            self._flag.set()

    async def _debounce_task(self):
        while True:
            await self._flag.wait()
            await asyncio.sleep_ms(self.debounce_ms)
            if self.pin.value() == 0 and self.callback:
                self.callback(self.button_name)

def on_button(name):
    print("Pressed:", name)

if __name__ == "__main__":
    print("Async button demo started")
    loop = asyncio.get_event_loop()
    loop.close()
    
    AsyncButton(15, callback=on_button, button_name="test_button")
    
    loop.run_forever()
