#import ubinascii

import gc
#import micropython


import uasyncio as asyncio
from client import TcpClient

#import utime as time

from config import Config
from led_control import LedBlinker
from status import Status
import sys
import utime
from machine import Pin


import logging
#import network


class ButtonBox:
  
  def __init__(self):
    self.log = logging.getLogger('main')
    self.log.info('starting ')

    print("Memory before Status:", gc.mem_free())
    gc.collect()
    print("Memory before Status:", gc.mem_free())
    self.status = Status()
    self.log.info('Config')
    print("Memory before Config:", gc.mem_free())
    gc.collect()
    print("Memory before Config:", gc.mem_free())
    self.config =  Config()
    self.log.info('Blinker')
    print("Memory before LedBlinker:", gc.mem_free())
    gc.collect()
    print("Memory before LedBlinker:", gc.mem_free())
    led_pin = "LED"
    if str(self.config.screen28) == "True":
      led_pin = 27
    self.led = LedBlinker(pin=led_pin)
    self.led.blink_fast()

    self.connected = False

    self.last_date_info_time = 0
  
    #check if we are in non-start mode
    if(self.config.mode == '0'):
      ## NOTE used to be status()
      self.config.mode = 1;
      self.config.save()
      sys.exit()
    
    self.client = None
    print(f'time {utime.time()} - last: {self.last_date_info_time}')
    
    self.log.info('TCP Client')
    self.client = TcpClient(self.text_received, self.status_update, self.cb)


    self.loop = asyncio.get_event_loop()
  
  def press(self, p):
    print('Button pressed!! ', p)
   
  def text_received(self, line):
    parts = line.split(' ')

     
    if(parts[0] == 'ACK'):
      return
  
    #blink the LED to show we got data
    self.led.blink()
    # self.log.debug('Line: ' + str(parts))
    
    if(parts[0] == 'Update'):
        self.log.debug('update display now')
        # self.log.debug(parts)
        zone = parts[1]
        on_off = parts[2]
        pin = None
        if zone == "Downstairs":
          pin = 0
        elif zone == "Upstairs":
          pin = 1
        else:
          return

        if on_off == "On":
          self.log.info(f'{zone} heating is ON')
          Pin(pin, Pin.OUT).value(1)
        else:
          self.log.info(f'{zone} heating is OFF')
          Pin(pin, Pin.OUT).value(0)

        print(f'Update command for zone {zone} to {on_off}')

  def status_update(self, wifi_connected, client_connected, ip):
    #NOTE: sometimes wifi status is reported as False even when 
    #      the client is connected and working perfectly
    #NOTE this returns no output if there is something wrong in the code - it just fails silently
      
    #print(f'>>> Status : {wifi_connected} - {client_connected} (ip:{ip})')
    
    status = 'Connected'
    self.status.wifi = wifi_connected
    if self.status.client == False and client_connected == True:
      #status has changed - make a request for date info
      self.client.send("DateTimeInfo\n")

    self.status.client = client_connected

    #print the IP to the screen, but only the first time we receive it
    if client_connected is False:
      if wifi_connected is False:
        status = 'WiFi...'
        self.led.blink_fast()
      else:

        status = 'Client...'
        self.led.blink_slow()

    
        
  
  def tidy_up(self):
    
      #some stuff to do when the program exits
      #turn the LED off
      self.led.off()
      self.sensor.close()
      self.client.close()
      self.led.close()
      
      self.log.info('All done!')

  def cb(self, x): 
    pass

def exception_handler(loop, context):
  log = logging.getLogger('main')
  exc = context.get('exception')
  if exc:
      log.error(f"Caught exception: {exc}")
      # Print the stack trace to the console or log it
      sys.print_exception(exc)
  else:
      log.error(f"Exception occurred without an explicit exception object: {context}")

t = None
try:

  #restart webrepl, it works better after wifi is connected (apparently)
  import gc
  #import webrepl
  #webrepl.start()
  gc.collect()
  
  print('Begin...')
  t = ButtonBox()
  print('ButtonBox created')
  gc.collect()
  
  loop = asyncio.get_event_loop()
  loop.set_exception_handler(exception_handler)
  loop.run_forever()
  
except BaseException as e:
  print('Exception : ' + str(e))
  print('E' + str(e.value))
  print('E' + str(e.errno))
  raise
except:
  print('Something else!')
  raise
finally:
  try:
    if t:
      t.tidy_up()
  finally:
    pass
  
  ##this code makes it auto reboot, but it also swallows errors
  ## maybe it should go in main??
  import time 
  print('Program finished, rebooting in 10 seconds (CTRL-c to cancel)')
  for x in range(10):
    print('.', end='')
    time.sleep(1)
  
  import machine
  machine.reset()
