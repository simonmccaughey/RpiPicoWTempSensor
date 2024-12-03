## This is support for the pimorini 2.8 display (not touchscreen)

import machine
import time
from pimoroni import RGBLED
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_RGB332
import logging

class TemperatureDisplay(object):
 
  #pin 5 is D1 and pin 4 is D2
  def __init__(self):
    self.log = logging.getLogger('Display28')
    self.log.info('Opening Display 2.8 pimorini=')
    
    self.display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, pen_type=PEN_RGB332)
    self.display.set_backlight(0.8)
  
    #for now turn the LED off
    led = RGBLED(26, 27, 28)
    led.set_rgb(0, 0, 0)

    BLACK = self.display.create_pen(0, 0, 0)
    WHITE = self.display.create_pen(255, 255, 255)
    self.display.set_pen(BLACK)
    self.display.clear()
    self.display.update()
      
  def cb(self, n):
    # self.text(str(n),113,17)
     
    self.log.info(f'TODO : display cb : {n}')

  def temperature(self, temperature):
    if self.display is not None:
      # Writer.set_textpos(16, 20)
      # self.writer.printstring(str(round(float(temperature),1)))
      # self.display.show()
      self.log.info(f'TODO : display temperature : {temperature}')
      display = self.display
      BLACK = display.create_pen(0, 0, 0)
      WHITE = display.create_pen(255, 255, 255)
      display.set_pen(BLACK)
      display.rectangle(1, 1, 100, 25)

      # writes the reading as text in the white rectangle
      display.set_pen(WHITE)
      display.set_font("sans")
      display.set_thickness(1)
      display.text(f"{temperature}", 10, 15, scale=1)

      # time to update the display
      display.update()
    
  def temperature_set(self, temperature):
    if self.display is None:
      return
    temp = round(float(temperature),1)
    if temp == -999.0:
      t = 'none'
    else:
      t = temp
    #extra space here to cover 'bottom_line_text'
    # self.text('t=%s     ' % t, 0,57)
    self.log.info(f'TODO : display SET temperature : {t}')
    display = self.display
    BLACK = display.create_pen(0, 0, 0)
    WHITE = display.create_pen(255, 255, 255)
    display.set_pen(BLACK)
    display.rectangle(1, 30, 100, 25)

    # writes the reading as text in the white rectangle
    display.set_pen(WHITE)
    display.set_font("sans")
    display.text(f"{t}", 10, 43, scale=1)

    # time to update the display
    display.update()


  def bottom_line_text(self, text):
    # self.text(text, 0,57)
    if self.display is None:
      return
    

    self.log.info(f'TODO : display bottom line text : {text}')

    self.tiny_status_text(text, top=230, left=250, width=100, height=10)

    # display = self.display
    # BLACK = display.create_pen(0, 0, 0)
    # WHITE = display.create_pen(255, 255, 255)
    # display.set_pen(BLACK)
    # display.rectangle(1, 160, 230, 25)

    # # writes the reading as text in the white rectangle
    # display.set_pen(WHITE)
    # display.set_font("bitmap8")
    # display.text(f"{text}", 10, 170, scale=1)

    # # time to update the display
    # display.update()
    
  def showprogram(self, on_off, time):
    if self.display is None:
      return
    #invert the colour if it is 'On'
    col = 0 if on_off == 'On' else 1
    #put a load of spaces along the display to colour it in
    if time == '00:00':
      #dont show the time if it is 00:00
      # self.text(on_off + '                                 ', 0,0, col)
      self.log.info(f'TODO : display prog : {on_off}/{time}')
    else:
      #self.text(on_off + '/' + time + '                    ', 0,0, col)
      self.log.info(f'TODO : display prog : {on_off}/{time}')

    display = self.display
    BLACK = display.create_pen(0, 0, 0)
    WHITE = display.create_pen(255, 255, 255)
    display.set_pen(WHITE)
    display.rectangle(1, 90, 230, 25)

    # writes the reading as text in the white rectangle
    display.set_pen(BLACK)
    display.set_font("sans")
    display.text(f"{on_off}/{time}", 10, 100, scale=1)

    # time to update the display
    display.update()

  

  def connection_status(self, status_text):
    # formatted = f'{status_text}                                  '
    #self.text(formatted, 0, 0, 0)
    # display = self.display
    # BLACK = display.create_pen(0, 0, 0)
    # WHITE = display.create_pen(255, 255, 255)
    # display.set_pen(WHITE)
    # top = 230
    # left = 10
    # height = 10
    # width = 100

    self.tiny_status_text(status_text, top=230, left=10, width=100, height=10)
    # display.rectangle(left-10, top-1, width, height)

    # # writes the reading as text in the white rectangle
    # display.set_pen(BLACK)
    # display.set_font("bitmap8")
    # display.text(f"{status_text}", left, top, scale=1.0)

    # # time to update the display
    # display.update()

  def tiny_status_text(self, status_text, top, left, height, width, invert=False):
    formatted = f'{status_text}                                  '
    #self.text(formatted, 0, 0, 0)
    display = self.display
    foreground = display.create_pen(0, 0, 0) #white
    background = display.create_pen(255, 255, 255) #black
    if invert:
      background, foreground = foreground, background
    display.set_pen(foreground)

    display.rectangle(left-10, top-1, width, height)

    # writes the reading as text in the white rectangle
    display.set_pen(background)
    display.set_font("bitmap8")
    display.text(f"{status_text}", left, top, scale=1.0)

    # time to update the display
    display.update()



  def time(self, time):
    if self.display is None:
      return
    #self.text(time, 89,57)
    self.log.info(f'TODO : display  time : {time}')
    display = self.display
    BLACK = display.create_pen(0, 0, 0)
    WHITE = display.create_pen(255, 255, 255)
    display.set_pen(WHITE)
    display.rectangle(1, 120, 100, 25)

    # writes the reading as text in the white rectangle
    display.set_pen(BLACK)
    display.set_font("sans")
    display.text(f"{time}", 10, 130, scale=1)

    # time to update the display
    display.update()

  def text(self, text, x, y, col=1):
    if self.display is None:
      return
    print(f'[Display]: {text}')
    if self.display is None:
      self.log.info(f'Fake display text: {text}')
    else:
      self.log.info(f'TODO : display : {text}')
      # fill_col = 1 - col
      # self.display.fill_rect(x, y, len(text)*8, 8, fill_col)
      # self.display.text(text, x, y, col)

      # self.display.show()
  def display_status(self):
    if self.display is None:
      return False
    return True
    
    
    
    
if __name__ == "__main__":

  display = TemperatureDisplay()
  display.temperature(23.2)
  display.temperature_set('12.4')
  display.connection_status('Connected')
  #display.cb(3)
  display.time('12:34')
  #display.text('On/10:23 ', 0,0, 0)
  #display.text('Off until 11:33', 0,0)
  display.text('t=24.5', 0,57)
  display.bottom_line_text("192.168.2.250")
  #display.text('22:33', 89,57)

  display.showprogram("On", "12:34")
  #display.text('Off/11:44', 0,0, 1)
  #display.text('           ', 0,0, 1)
  #display.text('On/10:23                                  ', 0,0, 0)

  #display.status('On', '12:22')
















