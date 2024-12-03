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
    self.display_temperature = "00.0"
    self.display_temperature_set = "00.0"
    self.display_bottom_line_text = ""
    self.display_status_text = "Initialising"
    self.display_time = "00:00"
    self.display_on_off = "Off"
    self.display_on_off_time = "00:01"
    self.display_day_of_week = "Sunday"

    self.display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, rotate=180)
    self.display.set_backlight(0.8)
  
    #for now turn the LED off
    led = RGBLED(26, 27, 28)
    led.set_rgb(0, 0, 0)


    ##TODO we can remove this clear and update
    BLACK = self.display.create_pen(0, 0, 0)
    self.display.set_pen(BLACK)
    self.display.clear()
    self.display.update()
    self.refresh()
      
  def cb(self, n):
    self.log.info(f'TODO : display cb : {n}')

  def refresh(self):
    if self.display is not None:
      display = self.display
      BLACK = display.create_pen(0, 0, 0)
      WHITE = display.create_pen(255, 255, 255)
      BACKGROUND = display.create_pen(140, 208, 235)
      DARK = display.create_pen(38, 130, 160)

      # draw the background
      display.set_pen(display.create_pen(232, 241, 244))
      display.rectangle(1, 1, 320, 240)
      display.set_pen(display.create_pen(245, 248, 249))
      display.rectangle(5, 5, 320-10, 240-10)
      display.set_pen(display.create_pen(175, 208, 220))
      display.rectangle(6, 6, 320-12, 240-12)
      display.set_pen(DARK)
      display.rectangle(7, 7, 320-14, 240-14)
      display.set_pen(display.create_pen(175, 208, 220))
      display.rectangle(8, 8, 320-16, 240-16)
      display.set_pen(BACKGROUND)
      display.rectangle(9, 9, 320-18, 240-18)
      

      #########################################################################
      ## Temperature Display
      self.log.info(f'TODO : display temperature : {self.display_temperature}')
      # display.set_pen(BACKGROUND)
      # display.rectangle(1, 1, 100, 25)

      # writes the reading as text in the white rectangle
      temperature_text = f"{self.display_temperature}"
      width = display.measure_text(temperature_text, scale=2)
      text_left = (320 // 2) - (width // 2) - 10
      
      display.set_font("sans")
      #draw the degrees symbol
      display.set_pen(DARK)
      display.set_thickness(4)
      display.text("o", 225, 75, scale=1)
      display.set_pen(WHITE)
      display.set_thickness(3)
      display.text("o", 225, 75, scale=1)
      display.set_thickness(1)


      #draw the actual text
      display.set_pen(DARK)
      display.set_thickness(9)
      display.text(temperature_text, text_left, 100, scale=2)
      display.set_pen(BACKGROUND)
      display.set_thickness(8)
      display.text(temperature_text, text_left, 100, scale=2)
      display.set_pen(WHITE)
      display.set_thickness(5)
      display.text(temperature_text, text_left, 100, scale=2)
      display.set_thickness(1)

      #########################################################################
      ## Temperature Set/Target Display

      self.log.info(f'TODO : display SET temperature : {self.display_temperature_set}')
      # display.set_pen(BACKGROUND)
      # display.rectangle(1, 30, 100, 25)

      # writes the reading as text in the white rectangle
      target_text = f"t={self.display_temperature_set}"
      width = display.measure_text(target_text, scale=0.8)
      text_left = (320 // 2) - (width // 2)

      display.set_font("sans")
      display.set_pen(DARK)
      display.set_thickness(3)
      display.text(target_text, text_left, 150, scale=0.8)
      display.set_pen(WHITE)
      display.set_thickness(2)
      display.text(target_text, text_left, 150, scale=0.8)
      display.set_thickness(1)


      #########################################################################
      ##  Bottom line text Display
      self.log.info(f'TODO : display bottom line text : {self.display_bottom_line_text}')

      self.tiny_status_text(self.display_bottom_line_text, top=222, left=240, width=80, height=10, foreground=BLACK, background=BACKGROUND)

      #########################################################################
      ##  Status text Display
      self.tiny_status_text(self.display_status_text, top=222, left=20, width=100, height=10, foreground=BLACK, background=BACKGROUND)

      #########################################################################
      ##  Time  Display

      self.log.info(f'TODO : display  time : {self.display_time}')
      # display.set_pen(WHITE)
      # display.rectangle(1, 120, 100, 25)

      # writes the reading as text in the white rectangle
      display.set_font("sans")
      display.set_pen(DARK)
      display.set_thickness(3)
      display.text(f"{self.display_time}", 10, 30, scale=0.9)
      display.set_pen(WHITE)
      display.set_thickness(2)
      display.text(f"{self.display_time}", 10, 30, scale=0.9)
      display.set_thickness(1)

      #########################################################################
      ##  Program  Display

      #TODO invert the colour or something if it is 'On'
      on_off_text = ""
      if self.display_on_off_time == '00:00':
        #dont show the time if it is 00:00
        on_off_text = "Off"
      else:
        on_off_text = f'{self.display_on_off} until {self.display_day_of_week[0:3]} {self.display_on_off_time}'
      self.log.info(f'TODO : display prog : {on_off_text}')

      # display.set_pen(WHITE)
      # display.rectangle(10, 200, 230, 25)

      # writes the reading as text in the white rectangle
      display.set_pen(BLACK)
      display.set_font("sans")
      display.text(on_off_text, 10, 200, scale=1)



      # time to update the display
      display.update()

    
    pass

  def temperature(self, temperature):
    self.display_temperature = temperature
    self.refresh()
    
  def temperature_set(self, temperature):
    if self.display is None:
      return
    temp = round(float(temperature),1)
    if temp == -999.0:
      t = 'none'
    else:
      t = temp
    self.display_temperature_set = t
    self.refresh()


  def bottom_line_text(self, text):

    self.display_bottom_line_text = text
    self.refresh()



    
  def showprogram(self, on_off, time, day_of_week):
    self.display_on_off = on_off
    self.display_on_off_time = time
    self.display_day_of_week = day_of_week

    self.refresh()
  

  def connection_status(self, status_text):
    self.display_status_text = status_text
    self.refresh()

  def tiny_status_text(self, status_text, top, left, height, width, foreground, background, invert=False):
    formatted = f'{status_text}                                  '
    #self.text(formatted, 0, 0, 0)
    display = self.display
    if invert:
      background, foreground = foreground, background
    display.set_pen(background)

    display.rectangle(left-10, top-1, width, height)

    # writes the reading as text in the white rectangle
    display.set_pen(foreground)
    display.set_font("bitmap8")
    display.text(f"{status_text}", left, top, scale=1.0)

  def time(self, time):
    self.display_time = time
    self.refresh()
    
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
  import time

  display = TemperatureDisplay()
  display.temperature(13.2)
  display.temperature_set('12.4')
  display.connection_status('Startup')
  display.time('12:34')
  display.bottom_line_text("192.168.2.250")
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

  #display.text('On/10:23 ', 0,0, 0)
  #display.text('Off until 11:33', 0,0)
  # display.text('t=24.5', 0,57)
  #display.text('22:33', 89,57)

  #display.text('Off/11:44', 0,0, 1)
  #display.text('           ', 0,0, 1)
  #display.text('On/10:23                                  ', 0,0, 0)

  #display.status('On', '12:22')
















