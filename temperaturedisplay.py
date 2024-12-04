from ssd1306 import SSD1306_I2C
import machine
from machine import I2C, Pin
from writer import Writer
import freesans34_num
import logging

class TemperatureDisplay(object):
 
  #pin 5 is D1 and pin 4 is D2
  def __init__(self, zone, sda_pin_num=8, scl_pin_num=9):
    self.log = logging.getLogger('Display')
    self.log.info('Opening I2C using sda=' + str(sda_pin_num) + ', scl=' + str(scl_pin_num))
    self.i2c = I2C(0, sda=Pin(sda_pin_num, machine.Pin.OUT), scl=Pin(scl_pin_num, machine.Pin.OUT))
    scan = self.i2c.scan()
    self.log.info('I2C Bus: ' + str(scan))
    
    if len(scan) == 0:
      self.log.info('No screen detected')
      self.display = None
    else:
      self.display = SSD1306_I2C(128, 64, self.i2c)
      self.display.contrast(0x01)
      #clear the screen
      self.display.fill(0)

      #display.text('Temperature',3,3)
      #self.display.text('00:00',75,57)
      self.writer = Writer(self.display, freesans34_num, verbose=False)
      Writer.set_clip(True, True)
      Writer.set_textpos(16, 20)
      #wri2.printstring('23.0')
      #write out the degrees sign on the screen (fixed location)
      self.display.text('O', 105, 17)

      self.display.show()
      
  def cb(self, n):
    self.text(str(n),113,17)

  def temperature(self, temperature):
    if self.display is not None:
      Writer.set_textpos(16, 20)
      self.writer.printstring(str(round(float(temperature),1)))
      self.display.show()
    
  def temperature_set(self, temperature):
    temp = round(float(temperature),1)
    if temp == -999.0:
      t = 'none'
    else:
      t = temp
    #extra space here to cover 'bottom_line_text'
    self.text('t=%s     ' % t, 0,57)

  def bottom_line_text(self, text):
    self.text(text, 0,57)

  def set_dates(self, day_of_week, month, mday, sunrise_time, sunset_time):
    pass

  def showprogram(self, on_off, time, day_of_week):
    #invert the colour if it is 'On'
    col = 0 if on_off == 'On' else 1
    #put a load of spaces along the display to colour it in
    if time == '00:00':
      #dont show the time if it is 00:00
      self.text(on_off + '                                 ', 0,0, col)
    else:
      self.text(on_off + '/' + time + '                    ', 0,0, col)
      

  def connection_status(self, text):
    if text == "Connected":
      return
    formatted = f'{text}                                  '
    self.text(formatted, 0, 0, 0)


  def time(self, time):
    self.text(time, 89,57)

  def text(self, text, x, y, col=1):
    print(f'[Display]: {text}')
    if self.display is None:
      self.log.info(f'Fake display text: {text}')
    else:
      fill_col = 1 - col
      self.display.fill_rect(x, y, len(text)*8, 8, fill_col)
      self.display.text(text, x, y, col)

      self.display.show()
  def display_status(self):
    if self.display is None:
      return False
    return True
    
    
    
    
if __name__ == "__main__":

  import time

  display = TemperatureDisplay("Upstairs")
  display.temperature(13.2)
  display.temperature_set('12.4')
  display.connection_status('Startup')
  #display.time('12:34')
  display.bottom_line_text("192.168.2.250")
  time.sleep(0.4)

  display.showprogram("On", "12:34", "Tuesday")
  #display.cb(3)
  time.sleep(0.4)
  display.temperature(23.3)
  display.connection_status('Wifi...')
  display.time('12:35')
  time.sleep(0.4)
  display.temperature(24.3)
  display.connection_status('Client...')
  display.time('12:36')
  time.sleep(0.4)
  display.temperature(25.3)
  display.connection_status('Connected')
  display.time('12:37')
  time.sleep(0.4)
  display.showprogram("Off", "21:11", "Wednesday")

  time.sleep(0.4)
  display.temperature_set('12.4')
















