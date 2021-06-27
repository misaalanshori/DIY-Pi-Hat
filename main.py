from luma.core.interface.serial import spi
from luma.lcd.device import pcd8544
from luma.core.render import canvas
from time import sleep
from PIL import ImageFont

import psutil
import socket
from datetime import datetime

from apps import piInfo
from config import *
from funcs import centerText
from funcs import posOffset as po

interface = spi(port=dispPort, device=dispDev, gpio_DC=dispDC, gpio_RST=dispRST)
disp = pcd8544(serial_interface=interface)
disp.capabilities(dispWidth, dispHeight, dispRotation)
disp.contrast(dispContrast)
disp.clear()

font = ImageFont.truetype(fontFile, fontSize)

appList = [piInfo]
currentPage = 0

while True:
	with canvas(disp) as draw:
		draw.rectangle(disp.bounding_box, outline="white")
		draw.rectangle((0, dispHeight, dispWidth, dispHeight - 8), outline="white", fill="white")
		centerText(draw, po(0,40)[1], "{}/{}".format(currentPage+1, len(appList)), "black", font)
		appList[currentPage](draw, font)
	sleep(0.25)
