import network
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('BTWholeHome-CJW', '1029384756abc')
sta_if.isconnected()
sta_if.ifconfig()




ap = network.WLAN(network.AP_IF)
ap.active(False)
#id = f'Thermostat_XXX' 
#ap.config(ssid=id, essid=id, password = '1029384756')
#ap.active(True)

