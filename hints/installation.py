
#this script is ran as part of the mpremote automated installation

import mip
mip.install("logging")
mip.install("ssd1306")
mip.install("pkg_resources")
mip.install("github:pfalcon/picoweb/picoweb/__init__.py", target="/lib/picoweb")
mip.install("github:pfalcon/picoweb/picoweb/utils.py", target="/lib/picoweb")

##end of instructions, below this is notes only.

#alternative to picoweb:
#mip.install('github:miguelgrinberg/microdot/src/microdot.py')
#mip.install('github:miguelgrinberg/microdot/src/microdot_asyncio.py')

#using mpremote to install modules on newer firmware
#mpremote connect /dev/ttyS4 mip install https://raw.githubusercontent.com/pfalcon/pycopy-lib/master/ulogging/ulogging.py
#mpremote connect /dev/ttyS4 mip install https://raw.githubusercontent.com/stlehmann/micropython-ssd1306/master/ssd1306.py

#for newer micropython
#import mip
#mip.install('webrepl')

#note to configure webrepl for the first time, create a boot.py file, and run:
#import webrepl_setup


