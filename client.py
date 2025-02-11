
import network
import usocket as socket
import utime as time
from watchdog import WDT

import uasyncio as asyncio
from config import Config
import logging
import sys


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

    self.s = None

    self.loop = asyncio.get_event_loop()

    #soft watchdog 1 minute (NOTE: current max supported is about 8 seconds)
    #self.wdt = WDT(timeout=60000)
    ##TODO use the real watchdog when it supports longer times
    self.wdt = WDT()
    self.cb(11)
    
    #set the network hostname
    network.hostname(config.zone)
    self.sta_if = network.WLAN(network.STA_IF)
    ##reset the network config (helps if the module thinks it has a .4.* address)
    self.sta_if.ifconfig(('0.0.0.0', '0.0.0.0', '0.0.0.0', '0.0.0.0'))
    self.wifi()
    self.cb(12)

    #self.sta_if.config(dhcp_hostname='Therm-%s' % self.zone)
    ## NOTE: enabling AP can bleed .4.x addresses onto network - dont do it!   
    #set the access point ID
    ap = network.WLAN(network.AP_IF)
    ap.active(False)
    #id = f'Thermostat_{self.zone}' 
    #ap.config(ssid=id, essid=id, password = '1029384756')
    #ap.active(True)
    
    self.cb(14)
    self.loop.create_task(self.run())
    self.loop.create_task(self.send_ack_loop())

    self.cb(15)

    self.update_status()
    
    print('Init Complete.')
    self.cb(20)

  
  def close(self):
    if self.s is not None:
      self.s.close()
    self.cb(90)
    
  def update_status(self):
    if self.status_callback is not None:
      wifi = self.sta_if.isconnected()
      #print('wifi ' + str(wifi))
      #print('CONN ' + str(self.connected))
      ip = None
      if wifi:
        ip = self.sta_if.ifconfig()[0]
      #print(f'callback: {wifi}, {self.connected}, {ip}')
      ##NOTE this returns no output if there is something wrong in the code of the callback
      self.status_callback(wifi, self.connected, ip)
      #print(f'callback completed.............{self.status_callback}')
  
  async def wifi(self):
    print('=================>>>>  initialising wifi')
    if not self.sta_if.isconnected():
      self.sta_if.active(False)
      await asyncio.sleep_ms(1000)
    self.sta_if.active(True)
    self.sta_if.connect(self.wireless_ssid, self.wireless_password)
    print('initialising wifi completed')

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
      print('Starting...' + str(self.host)  + ':' + str(self.port))
      self.update_status()
      self.cb(30)
      await self.wifi()
     
      wifi_iterations = 0

      while True:
        try:
          self.cb(40)
          await asyncio.sleep_ms(1000)
          self.cb(50)
          self.update_status()
          if(self.sta_if.isconnected() == False):
            print('Not connected...')
            wifi_iterations += 1
            if(wifi_iterations > 10):
              wifi_iterations = 0
              await self.wifi()
              
          self.update_status()

          # Address lookup after wifi connection, and inside try/except block
          print('get address')
          addr_info = socket.getaddrinfo(self.host, self.port)
          addr = addr_info[0][-1]
          print(f'got address {addr}')
          
          print('Trying to connect to ' + str(addr))
          #display.status(str(addr))
          self.s = socket.socket()
          self.s.connect(addr)
      
          #TODO - client name here should be a single string
          self.s.write("ClientName %s-%s\n" % (self.client_name, self.zone))
          print('Connected!')
          print('' + str(self.sta_if.ifconfig()))
          #send an ack to get the time straight away
          self.send("ACK time\n")
          self.cb(51)
          sreader = asyncio.StreamReader(self.s)
          while True:
            await asyncio.sleep_ms(100)
            self.cb(60)
            self.update_status()
            self.cb(61)
            line = await sreader.readline()
            print('Recieved' + str(line))
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
          print('environment exception : ' + str(e) + ' Wifi:' + str(self.sta_if.isconnected()))
          
          self.update_status()
          self.cb(84)
        finally:
          await asyncio.sleep_ms(5000)
          self.cb(85)
    except BaseException as e:
      print(f'Exception : {e} ' + str(e))
      raise e
          
    finally:
      #some stuff to do when the program exits
      
      self.cb(86)
      if self.s is not None:
        self.s.close()
        self.cb(87)
      print('All done!')

          
def rx(line):
  print('Handler: Received line: ' + str(line))

def cb(line):
  #print('DEBUG: Received line: ' + str(line))
  pass

def status_main(wifi_connected, client_connected, ip):
  print('>>> Status : ' + str(wifi_connected) + ' - ' + str(client_connected))
 
def exception_handler(loop, context):
  log = logging.getLogger('main')
  exc = context.get('exception')
  if exc:
      log.error(f"Caught exception: {exc}")
      # Print the stack trace to the console or log it
      sys.print_exception(exc)
  else:
      log.error(f"Exception occurred without an explicit exception object: {context}")

 
if __name__ == "__main__":
  
  from client import TcpClient
  c = TcpClient(rx, status_main, cb=cb)
  
  loop = asyncio.get_event_loop()
  loop.set_exception_handler(exception_handler)
  #asyncio.set_debug(False)
  loop.run_forever()
















