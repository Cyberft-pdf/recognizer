import pywifi
from pywifi import const

wifi = pywifi.PyWiFi()
iface = wifi.interfaces()[0]  

iface.scan() 
iface.scan_results()

scan_results = iface.scan_results()
for result in scan_results:
    ssid = result.ssid
    signal_strength = result.signal
    print(f"SSID: {ssid}, Signál: {signal_strength} dBm")
