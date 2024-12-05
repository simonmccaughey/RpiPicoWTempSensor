## This is support for the pimorini 2.8 display (not touchscreen)

import time
# from pimoroni import RGBLED
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_RGB332
import logging
import time
import gc
#import webrepl
#webrepl.start()


class TemperatureDisplay(object):
 
  #pin 5 is D1 and pin 4 is D2
  def __init__(self, zone):
    self.log = logging.getLogger('Display28')
    self.log.info('Opening Display 2.8 pimorini=')
    self.display_zone = zone
    self.display_temperature = "00.0"
    self.display_temperature_set = "none"
    self.display_bottom_line_text = ""
    self.display_status_text = "Initialising"
    self.display_time = None
    self.display_on_off = "???"
    self.display_on_off_time = "00:00"
    self.display_day_of_week = "Sunday"
    ##this is the format
    # self.formatted_date = "Mon Nov 22"
    self.formatted_date = None
    self.sunrise = "0500"
    self.sunset = "2300"
    ## this is the one that comes from the server
    self.day = ""

    self.display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, rotate=180)
    self.display.set_backlight(0.8)
  
    #for now turn the LED off (removed this for memory efficiency)
    # led = RGBLED(26, 27, 28)
    # led.set_rgb(0, 0, 0)
    # self.led = led
      
  def cb(self, n):
    self.log.info(f'TODO : display cb : {n}')

  def compare_times(self, time1, time2):
    return int(time1.replace(":", "")) < int(time2.replace(":", ""))

  def refresh(self):
    gc.collect()
    self.check_free_mem()

    if self.display is not None:
      display = self.display

      daytime = True
      ##check if we have time info, and if it is day or night
      if self.display_time and (self.compare_times(self.display_time, self.sunrise) or self.compare_times(self.sunset, self.display_time)):
        daytime = False

      BLACK = display.create_pen(0, 0, 0)
      WHITE = display.create_pen(255, 255, 255) if daytime else display.create_pen(180, 180, 180)
      BACKGROUND = display.create_pen(140, 208, 235) if daytime else display.create_pen(20, 50, 70)
      DARK = display.create_pen(38, 130, 160)



      # if self.display_on_off == 'On':
      #   BACKGROUND = display.create_pen(235, 130, 120)
      OUTSIDE_BORDER = display.create_pen(232, 241, 244) if daytime else display.create_pen(150, 150, 150)
      BOTTOM_BAND = BLACK
      PROG_BACKGROUND = BACKGROUND
      if self.display_on_off == 'On':
        #make the wee band be red
        RED = display.create_pen(235, 0, 0)
        OUTSIDE_BORDER = RED
        BOTTOM_BAND = RED
        PROG_BACKGROUND = RED

      # draw the background
      display.set_pen(OUTSIDE_BORDER)
      display.rectangle(1, 1, 320, 240)
      line = display.create_pen(245, 248, 249)  if daytime else BLACK
      display.set_pen(line)
      display.rectangle(5, 5, 320-10, 230-10)
      line = display.create_pen(245, 248, 249)  if daytime else display.create_pen(180, 180, 180)
      display.set_pen(line)
      display.rectangle(6, 6, 320-12, 230-12)
      display.set_pen(DARK)
      display.rectangle(7, 7, 320-14, 230-14)
      display.set_pen(line)
      display.rectangle(8, 8, 320-16, 230-16)
      display.set_pen(BACKGROUND)
      display.rectangle(9, 9, 320-18, 230-18)
      
      #########################################################################
      ## Zone name Display

      # zone_text = self.display_zone
      # width = display.measure_text(zone_text, scale=0.9)
      # text_left = (320 // 2) - (width // 2)

      # display.set_font("sans")
      # display.set_pen(DARK)
      # display.set_thickness(3)
      # display.text(zone_text, text_left, 70, scale=0.9)
      # display.set_pen(WHITE)
      # display.set_thickness(2)
      # display.text(zone_text, text_left, 70, scale=0.9)
      # display.set_thickness(1)


      #########################################################################
      ## Temperature Display
      self.log.info(f'TODO : display temperature : {self.display_temperature}')
      # display.set_pen(BACKGROUND)
      # display.rectangle(1, 1, 100, 25)

      # writes the reading as text in the white rectangle
      temperature_text = f"{self.display_temperature}"
      width = display.measure_text(temperature_text, scale=2)
      text_left = (320 // 2) - (width // 2) - 10
      top = 105
      
      display.set_font("sans")
      #draw the degrees symbol
      display.set_pen(DARK)
      display.set_thickness(4)
      display.text("o", 230, top-25, scale=1)
      display.set_pen(WHITE)
      display.set_thickness(3)
      display.text("o", 230, top-25, scale=1)
      display.set_thickness(1)

      #draw the actual temperature text
      scale = 2.2
      display.set_pen(DARK)
      display.set_thickness(9)
      display.text(temperature_text, text_left, top, scale=scale)
      display.set_pen(BACKGROUND)
      display.set_thickness(8)
      display.text(temperature_text, text_left, top, scale=scale)
      display.set_pen(WHITE)
      display.set_thickness(5)
      display.text(temperature_text, text_left, top, scale=scale)
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
      display.text(target_text, text_left, 152, scale=0.8)
      display.set_pen(WHITE)
      display.set_thickness(2)
      display.text(target_text, text_left, 152, scale=0.8)
      display.set_thickness(1)

      #########################################################################
      ##  Bottom line text Display - black line
      display.set_pen(BOTTOM_BAND)

      display.rectangle(1, 230, 320, 240)

      #########################################################################
      ##  Bottom line text Display
      self.log.info(f'TODO : display bottom line text : {self.display_bottom_line_text}')
      self.tiny_status_text(self.display_bottom_line_text, top=232, left=240, width=80, height=10, right=320, foreground=WHITE, background=BLACK)

      #########################################################################
      ##  Status text Display
      status_text = f'{self.display_zone}: {self.display_status_text}'
      self.tiny_status_text(status_text, top=232, left=2, width=100, height=10, right=None, foreground=WHITE, background=BLACK)

      #########################################################################
      ##  Time  Display

      self.log.info(f'TODO : display  time : {self.display_time}')
      # display.set_pen(WHITE)
      # display.rectangle(1, 120, 100, 25)

      # writes the reading as text in the white rectangle
      display_time = self.display_time if self.display_time else "--:--"

      display.set_font("sans")
      display.set_pen(DARK)
      display.set_thickness(3)
      display.text(f"{display_time}", 10, 22, scale=0.7)
      display.set_pen(WHITE)
      display.set_thickness(2)
      display.text(f"{display_time}", 10, 22, scale=0.7)
      display.set_thickness(1)

      #########################################################################
      ##  Date / Day  Display

      date_time = self.formatted_date
      if date_time:
        width = display.measure_text(date_time, scale=0.7)
        #print(f"width:{width}")

        display.set_font("sans")
        display.set_pen(DARK)
        display.set_thickness(3)
        display.text(date_time, 310-width, 22, scale=0.7)
        display.set_pen(WHITE)
        display.set_thickness(2)
        display.text(date_time, 310-width, 22, scale=0.7)
        display.set_thickness(1)

      #########################################################################
      ##  Program  Display

      #TODO invert the colour or something if it is 'On'
      on_off_text = ""
      if self.display_on_off_time == '00:00':
        #dont show the time if it is 00:00
        on_off_text = self.display_on_off # use the actual value, as it might be startup text
      elif self.display_on_off == "On":
        on_off_text = f'{self.display_on_off} until {self.display_on_off_time}'
      elif self.display_on_off == "Off":
        on_off_text = f'{self.display_on_off} until {self.display_day_of_week[0:3]} {self.display_on_off_time}'.replace(f'{self.day} ', '')
      self.log.info(f'TODO : display prog : {on_off_text}')

      width = display.measure_text(on_off_text, scale=0.8)
      text_left = (320 // 2) - (width // 2)

      display.set_pen(PROG_BACKGROUND)
      display.rectangle(text_left-5, 186, width+10, 28)
      display.circle(text_left-5, 186+13, 13)
      display.circle(text_left+width+5, 186+13, 13)


      display.set_font("sans")
      display.set_pen(DARK)
      display.set_thickness(3)
      display.text(on_off_text, text_left, 200, scale=0.8)
      display.set_pen(WHITE)
      display.set_thickness(2)
      display.text(on_off_text, text_left, 200, scale=0.8)



      # time to update the display
      display.update()

    
    pass
  def brightness(self, value):
      print(f"Display brightness set to {value}")
      self.display.set_backlight(value)

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


  def set_dates(self, day_of_week, month, mday, sunrise_time, sunset_time):
    print(f'times received: day:{day_of_week} month:{month} mday:{mday} rise:{sunrise_time} set:{sunset_time}')
    self.sunrise = sunrise_time
    self.sunset = sunset_time
    self.formatted_date = f'{day_of_week[0:3]} {month[0:3]} {mday}'
    self.day = day_of_week[0:3]
    
  def showprogram(self, on_off, time, day_of_week):
    self.display_on_off = on_off
    self.display_on_off_time = time
    self.display_day_of_week = day_of_week

    self.refresh()
  
  def check_free_mem(self):
    import gc
    gc.collect()
    F = gc.mem_free()
    A = gc.mem_alloc()
    T = F + A
    # largest = gc.mem_free()  # Measure the largest free block
    P = '{0:.2f}%'.format(F / T * 100)
    # print(f"Total RAM: {T} bytes")
    print(f"Unused RAM: {F} bytes ({P} free)")
    # print(f"Largest Free Block: {largest} bytes")

  def connection_status(self, status_text):
    self.display_status_text = status_text
    self.refresh()

  def tiny_status_text(self, status_text, top, left, right, height, width, foreground, background, invert=False):
    display = self.display
    if invert:
      background, foreground = foreground, background
    display.set_pen(background)
    display.set_font("bitmap8")

    if right is not None:
      ##this is right aligned text, figure out the width
      width = display.measure_text(status_text, scale=1)
      left = (right) - (width)
      #print(f"for text {status_text} width:{width} left:{left}")

    # display.rectangle(left-10, top-1, width, height)

    # writes the reading as text in the white rectangle
    display.set_pen(foreground)
    display.text(f"{status_text}", left, top, scale=1)

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

  display = TemperatureDisplay("Upstairs")
  display.temperature(13.2)
  display.temperature_set('12.4')
  display.connection_status('Startup')
  display.time('12:34')
  display.bottom_line_text("192.168.2.250")
  display.showprogram("On", "12:34", "Tuesday")
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
  display.set_dates("Tuesday", "November", "24", "0900", "1600")
  display.time('00:36')
  time.sleep(0.4)
  display.time('12:36')
  time.sleep(0.4)
  display.time('22:36')
  time.sleep(0.4)
  display.showprogram("On", "12:34", "Tuesday")
  
  ##This is the same code that should be in the main class
  #            0        1     2         3   4          5              6
  line = "DateTimeInfo 2024 December|12 04 Wednesday sunrise|08:34 sunset|16:01"
  parts = line.split(' ')
  #day_of_week, month, mday, sunrise_time, sunset_time
  display.set_dates(parts[4], parts[2].split("|")[0], parts[3], parts[5].split("|")[1], parts[6].split("|")[1])
  
  display.showprogram("On", "12:34", "Tuesday")















