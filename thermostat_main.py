#import ubinascii

import gc
#import micropython


import uasyncio as asyncio
from client import TcpClient
from tempsensor import TempSensor

#import utime as time

from config import Config
from led_control import LedBlinker
from status import Status
import sys
import utime
from machine import Pin


import logging
#import network


class Thermostat:
  
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
    self.zone = self.config.zone

    self.set_temp = 0
    self.log.info('Display')
    #NOTE: we cant detect the 2.8 pimorini screen, so we just have to configure it
    if str(self.config.screen28) == "True":
      print("import 2.8 <<<<<<<<<<<")
      from temperaturedisplay28 import TemperatureDisplay
    else:
      print("import regular <<<<<<<<<<<")
      from temperaturedisplay import TemperatureDisplay
    print("Memory before TemperatureDisplay:", gc.mem_free())
    gc.collect()
    print("Memory before TemperatureDisplay:", gc.mem_free())
    self.display = TemperatureDisplay(self.zone)
    self.brightness = float(self.config.brightness_0_1)
    self.display.brightness(self.brightness)

    #display the version briefly at startup
    self.display.bottom_line_text('241204 2200 2.8 LCD')
    self.last_date_info_time = 0
  
    #check if we are in non-start mode
    if(self.config.mode == '0'):
      ## NOTE used to be status()
      self.display.connection_status('Connect mode')
      self.config.mode = 1;
      self.config.save()
      sys.exit()

    
    self.log.info('Sensor')
    print("Memory before TempSensor:", gc.mem_free())
    gc.collect()
    print("Memory before TempSensor:", gc.mem_free())
    self.sensor = TempSensor(self.read_temp)
    self.sensor.auto_report = self.config.auto_report
    
    self.client = None
    print(f'time {utime.time()} - last: {self.last_date_info_time}')

    #D0	16
    #D1	5
    #D2	4
    #D3	0
    #D4	2
    #D5	14
    #D6	12
    #D7	13
    #D8	15
    #TX	1
    #RX	3
    #self.setup(14, 1)
    #self.setup(12, 2)
    #self.setup(13, 3)
    #self.setup(15, 4)
    #self.setup(2,  5)
    
    self.display.connection_status('Starting...')
    self.log.info('TCP Client')
    self.client = TcpClient(self.text_received, self.status_update, self.cb)

    boost_pin = Pin(15, Pin.IN, Pin.PULL_UP)  
    off_pin = Pin(14, Pin.IN, Pin.PULL_UP)  
    increase_pin = Pin(13, Pin.IN, Pin.PULL_UP)  
    decrease_pin = Pin(12, Pin.IN, Pin.PULL_UP)  
    boost_pin.irq(trigger=Pin.IRQ_FALLING, 
                          handler=lambda pin: self.client.send(f"Boost {self.zone}\n"))
    off_pin.irq(trigger=Pin.IRQ_FALLING, 
                          handler=lambda pin: self.client.send(f"SetZoneOff {self.zone}\n"))
    increase_pin.irq(trigger=Pin.IRQ_FALLING, 
                          handler=lambda pin: self.adjust_brightness(0.1))
    decrease_pin.irq(trigger=Pin.IRQ_FALLING, 
                          handler=lambda pin: self.adjust_brightness(-0.1))


    self.loop = asyncio.get_event_loop()
    self.loop.create_task(self.uptime())
    self.loop.create_task(self.print_status())
  def adjust_brightness(self, delta):
      # Adjust brightness within the range [0.0, 1.0]
      new_brightness = round(max(0.0, min(1.0, self.brightness + delta)), 1)
      if new_brightness != self.brightness:  # Only update if there is a change
          self.brightness = new_brightness
          self.display.brightness(self.brightness)  # Call display method
          self.config.brightness_0_1 = self.brightness
          self.config.save()
          print(f"Brightness set to {self.brightness}")
  
  def press(self, p):
    print('Button pressed!! ', p)

  
  # def setup(self, gpio, no):
  #   pin = Pin(gpio, Pin.IN, machine.Pin.PULL_UP)
  #   pb = Pushbutton(pin, self.press, (no,))

  def read_temp(self, temp):
    
    print('temperatures:', end=' ')
    try:
      print(temp, end=' ')
      self.display.temperature(temp)
      self.status.temp = temp
      print('about to send', end=' ')
      self.client.send("TempRead %s %s\n" % (self.zone, temp))
      self.log.info('sent : ' + str(temp))
    except BaseException as e:
      self.log.warning("Unexpected error:" + str(e))
    except :
      self.log.warning("Super-Unexpected error:")
        #pass
    print('')

  def button_pressed(self, pin):
    
    ##TODO up/down setting on 2 pins
    self.set_temp += 0.5
    self.log.info('new temp ' + str(self.set_temp))
    #if client_connected:
    #  client.send("TempSet %s %s\n" % (zone, set_temp))

  def cb(self, n):
    pass
    #self.display.cb(n)
    
  def text_received(self, line):
    parts = line.split(' ')

     
    if(parts[0] == 'ACK'):
      time = parts[2][0:5]
      self.display.time(time)
      self.status.last_time = parts[2]


      # ##check if we need to request DateTimeInfo (used to display day/month at top right)
      # Request after midnight, and not within an hour of previous request
      if (utime.time() - self.last_date_info_time > 3600) and time.startswith('00'):
        print("requesting DateTimeInfo")
        self.client.send("DateTimeInfo\n")
      else:
        print("NOT requesting DateTimeInfo")

      return # so we dont blink the LED
  
    #blink the LED to show we got data
    self.led.blink()
    self.log.debug('Line: ' + str(parts))
    
    if(parts[0] == 'Update'):
      if(parts[1] == self.zone):
        self.log.debug('update display now')
        time = parts[3][0:5]
        self.log.info('program time : ' + time)
        ##TODO add Day as arg to other display, so it supports the arg (it can ignore it)
        self.display.showprogram(parts[2], time, parts[4])
        self.set_temp = parts[6]
        self.display.temperature_set(self.set_temp)
        self.status.set_temp = self.set_temp
        self.status.time = time
        self.status.state = parts[2]
        self.display.connection_status("Connected")

    if(parts[0] == 'DateTimeInfo'):
      #    0          1      2        3   4      5              6
      #DateTimeInfo 2024 November|11 24 Monday sunrise|07:00 sunset|22:00
      self.display.set_dates(parts[4], parts[2].split("|")[0], parts[3], parts[5].split("|")[1], parts[6].split("|")[1])
      self.last_date_info_time = utime.time()

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
    if ip is not None and self.status.ip is None:
      self.status.ip = ip
      #print it a load of times, if another event comes in, it will overwrite it.
      for x in range(60):
        #TODO I removed a load of spaces from the end of this - needs fixed for other screen
        self.display.bottom_line_text(f'{ip}')
    if client_connected is False:
      if wifi_connected is False:
        status = 'WiFi...'
        self.led.blink_fast()
      else:

        status = 'Client...'
        self.led.blink_slow()
      ##NOTE: used to be status()
      self.display.connection_status(status)
    #print('=== callback complete ===')

  async def uptime(self):
    minutes = 0
    while(True):
      await asyncio.sleep(60)
      minutes += 1
      self.log.info('Uptime: ' + '{:02d}h:{:02d}m'.format(*divmod(minutes, 60)))
      
        
  async def print_status(self):
    while(True):
      await asyncio.sleep_ms(2000)
      self.status.screen = self.display.display_status()
      self.status.sensor = self.sensor.sensor_status()
      
      #self.status.print()
  
  def tidy_up(self):
    
      #some stuff to do when the program exits
      #turn the LED off
      self.led.off()
      self.sensor.close()
      self.client.close()
      self.led.close()
      self.display.connection_status('Program closed')
      
      self.log.info('All done!')


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
  t = Thermostat()
  print('Thermostat created')
  gc.collect()
  #import pico_web
  
  loop = asyncio.get_event_loop()
  loop.set_exception_handler(exception_handler)
  #loop.run_forever()
  #gc.collect()
  print('import web...')
  import pico_web
  gc.collect()
  print('import completed')
  pico_web.myWs.set_status(t.status)
  pico_web.app.run(debug=True, host='0.0.0.0', port=80)
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

















