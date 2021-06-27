from luma.core.interface.serial import spi
from luma.lcd.device import pcd8544
from luma.core.render import canvas
from time import sleep
from PIL import ImageFont

import psutil
import socket
from datetime import datetime

from apps import piInfo

interface = spi(port=0, device=0, gpio_DC=23, gpio_RST=24)
disp = pcd8544(serial_interface=interface)
disp.capabilities(84, 48, 2)
disp.contrast(60)
disp.clear()

font = ImageFont.truetype("TinyPixy.ttf", 10)

appList = [piInfo]

while True:
	with canvas(disp) as draw:
		draw.rectangle(disp.bounding_box, outline="white")
		appList[0](draw, font)
	sleep(0.25)
