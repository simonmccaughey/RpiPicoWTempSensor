
import network
import usocket as socket
import utime as time
from watchdog import WDT

import uasyncio as asyncio
from config import Config
import ulogging as logging


class TcpClient:
  
  def __init__(self, callback=None, status_callback=None, cb=None):
    self.log = logging.getLogger('TcpClient')
    config =  Config()
    self.cb = cb
    self.cb(10)
    self.callback = callback
    self.status_callback = status_callback
    self.wireless_ssid = config.wifi_ssid
    self.wireless_password = config.wifi_password
    self.host = config.host
    self.port = int(config.port)
    self.client_name = config.client_name
    self.zone = config.zone
    self.ip = None
    
    self.connected = False
    self.sta_if = network.WLAN(network.STA_IF)
    self.wifi()
    #soft watchdog 1 minute (NOTE: current max supported is about 8 seconds)
    #self.wdt = WDT(timeout=60000)
    ##TODO use the real watchdog when it supports longer times
    self.wdt = WDT()
    

    #self.sta_if.config(dhcp_hostname='Therm-%s' % self.zone)
    
    #set the access point ID (might not work)
    #a = network.WLAN(network.AP_IF)
    #a.config(essid='Thermostat-%s' % self.zone)
    #a.active(True)
    
    self.loop = asyncio.get_event_loop()
    self.loop.create_task(self.run())
    self.loop.create_task(self.send_ack_loop())
    
    self.update_status()
    
    
    self.log.info('Client initialised')
    self.cb(20)
    

    self.s = None
    

  
  def close(self):
    self.s.close()
    self.cb(90)
    
  def update_status(self):
    if self.status_callback is not None:
      wifi = self.sta_if.isconnected()
      #print('wifi ' + str(wifi))
      #print('CONN ' + str(self.connected))
      self.status_callback(wifi, self.connected, self.ip)
  
  def wifi(self):
    self.sta_if.active(True)
    self.sta_if.connect(self.wireless_ssid, self.wireless_password)
    
  
  def do_connect(self):
    if not self.sta_if.isconnected():
        self.log.info('connecting to network...')
        self.cb(10)
        self.wifi()
        #wait a maximum number of times before failing
        for x in xrange(100):
          if self.sta_if.isconnected():
            self.wdt.feed()
            break;
          self.cb(11)
          await asyncio.sleep(0)
          time.sleep_ms(200)
    self.log.info('network config:' + str(self.sta_if.ifconfig()))
    self.cb(12)
    self.ip = self.sta_if.ifconfig()[0]
    self.cb(13)
    
  async def send_ack_loop(self):
    #print("in ack block " + str(self.connected))
    while(True):
      try:
        await asyncio.sleep_ms(1500)
        self.cb(63)
        await asyncio.sleep_ms(1500)
        self.send("ACK time\n")
        self.cb(64)
      except OSError as e:
        self.connected = False
        self.cb(65)
      

  def send(self, text):
    #print('client send...' + str(self.connected))
    if self.connected:
      #print('client sent1')
      self.s.write(text)
      #print('client sent2')
      
    
  async def run(self):
    
    try:
  
      #TODO - send proper status for wifi / client disconnection
      self.log.info('Starting...' + str(self.host)  + ':' + str(self.port))
      self.update_status()
      self.do_connect()
      self.update_status()
      self.cb(30)
     
      addr_info = socket.getaddrinfo(self.host, self.port)
      addr = addr_info[0][-1]

      while True:
        try:
          self.cb(40)
          await asyncio.sleep_ms(1000)
          self.cb(50)
          self.update_status()
          if(self.sta_if.isconnected() == False):
            self.do_connect()
          self.update_status()

          self.log.info('Trying to connect to ' + str(addr))
          #display.status(str(addr))
          self.s = socket.socket()
          self.s.connect(addr)
      
          #TODO - client name here should be a single string
          self.s.write("ClientName %s-%s\n" % (self.client_name, self.zone))
          self.log.info('Connected!')
          #send an ack to get the time straight away
          self.send("ACK time\n")
          self.cb(51)
          sreader = asyncio.StreamReader(self.s)
          while True:
            yield from asyncio.sleep(0)
            self.cb(60)
            self.update_status()
            self.cb(61)
            line = await sreader.readline()
            #print('Recieved', line)
            self.cb(70)

            line = line.decode('utf-8').rstrip()
            #print('Recieved ['+ line+ ']')
            if line == '':
              self.cb(71)
              raise OSError('empty data returned from socket')
            if self.callback is not None:  
              self.connected = True
              #tell the watchdog we are alive
              self.cb(80)
              ##TODO feed the dog
              self.wdt.feed() 
              self.callback(line)
              self.cb(81)
             
            await asyncio.sleep_ms(50)
            self.cb(82)
           
        except OSError as e:
          self.connected = False
          self.cb(83)

          #this happens if the WIFI disconnects, or if the socket disconnects
          self.log.info('environment exception : ' + str(e) + ' Wifi:' + str(self.sta_if.isconnected()))
          
          self.update_status()
          self.cb(84)
        finally:
          await asyncio.sleep_ms(5000)
          self.cb(85)
    finally:
      #some stuff to do when the program exits
      #turn the LED off
      #led.value(1)
      #Stop the timer, in case it's blinking
      #tim.deinit()
      #timer_temperature.deinit()
      self.cb(86)
      if self.s is not None:
        self.s.close()
        self.cb(87)
      self.log.info('All done!')

          
def rx(line):
  print('Handler: Received line: ' + str(line))

def cb(line):
  pass
  #print('Handler: Received line: ' + str(line))


if __name__ == "__main__":
  
  from client import TcpClient
  c = TcpClient(rx, cb=cb)
  
  loop = asyncio.get_event_loop()
  #asyncio.set_debug(False)
  loop.run_forever()












