

from ds18x20 import DS18X20
from onewire import OneWire
from machine import Pin
import uasyncio as asyncio

import logging

class TempSensor(object):
  
  def __init__(self, callback=None):
    self.log = logging.getLogger('TempSensor')
    self.log.info("starting...")
    ow = OneWire(Pin(22, Pin.IN, Pin.PULL_UP))

    self.auto_report = True
    self.callback = callback
    self.ds = DS18X20(ow)
    self.roms = None
    print("scanning for 1-wire devices...")
    
    #TODO make this write a sensible error when no device is found
    #self.timer_temperature = Timer(3)
    #self.timer_temperature.init(period=5000, mode=Timer.PERIODIC, callback=self.read_temp)  
    self.last_temps = []
    self.loop = asyncio.get_event_loop()
    self.loop.create_task(self.run_temp_sensor())

  #turn auto report off to switch to one minute max reporting
  def auto_report(self, true_or_false):
    self.auto_report = true_or_false
  
  def set_debug():
    log.setLevel(logging.DEBUG)
    
  def sensor_status(self):
    if len(self.roms) > 0:
      return True
    return False

  def close(self):
    #self.timer_temperature.deinit()
    print('TempSensor: Stopping timer')

  async def run_temp_sensor(self):    
    counter = 0
    while self.roms is None or len(self.roms) == 0:
      try:
        counter += 1
        if(counter > 10):
          await asyncio.sleep(10)
        await asyncio.sleep(1)
        print('Scanning for ROMs [attempt:' + str(counter) + ']')
        self.roms = self.ds.scan()
        print("found " + str(self.roms))
        
      except BaseException as e:
        self.log.error("Exception reading ROMs:" + str(e))
        
    
    
    #print('temperatures:', end=' ')
    counter = 0
    while True:
      self.log.debug("---------------------")
      try:
        
        self.ds.convert_temp()
        #print("sleep for 1")
        await asyncio.sleep_ms(1000)
        #print("sleep done")
        for rom in self.roms:
          #print("checking rom.." , rom)
          temp = self.ds.read_temp(rom);
          temp = str(round(float(temp),1))
          self.log.debug('Last: ' + str(self.last_temps) + ' - now: ' + str(temp)) 
          #counter makes us send something around every minute, even if the temperature hasnt changed
          counter += 1
          need_to_report = False
          
          #print(f'Self auto report : {self.auto_report} temp:{temp} [{self.last_temps}]')
          ##NOTE auto report looks boolean, but is actually string.
          if(str(self.auto_report) == 'True'):
            #print('in autoreport block')
            if(temp not in self.last_temps and temp is not None):
              #print('in new temperature block')
              need_to_report = True
              self.last_temps.insert(0, temp)
              if(len(self.last_temps) > 10):
                self.last_temps.pop()
              #print('TempSensor: ' + temp, end=' ')

              #print('about to report', end=' ')
          if(counter > 60):
            need_to_report = True
          #For debug - force report every time
          # need_to_report = True
          
          self.log.debug('counter : ' + str(counter) + ', need to report : ' + str(need_to_report)) 
          if(need_to_report):
            counter = 0
            self.loop.create_task(self.run_callback(temp))

      except BaseException as e:
        self.log.warning("Unexpected error:" +  str(e))
        await asyncio.sleep_ms(500)
      except :
        self.log.warning("Super-Unexpected error:")
          #pass
      #print('')
  async def run_callback(self, temp):
    if self.callback is not None:
      self.log.info('reporting...' + temp)
      #print("calling loop")
      self.callback(temp)
      self.log.debug('reported')

def my_callback(temp):
  print('>>>>> ' + temp)
  
def mysleep():
  await asyncio.sleep_ms(1000)

if __name__ == "__main__":
  #reset the event loop (otherwise lots of tasks run at the same time)
  ##NOTE: currently not working - do a soft reset between runs
  loop = asyncio.get_event_loop()
  loop.close()
  
  #optionally configure extra logging
  logging.basicConfig(level=logging.DEBUG)
  sensor = TempSensor(my_callback)
  
  loop.run_forever()











