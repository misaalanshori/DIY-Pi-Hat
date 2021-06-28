from luma.core.interface.serial import spi
from luma.lcd.device import pcd8544
from luma.core.render import canvas
from time import sleep
from PIL import ImageFont
import wiringpi

import apps
from config import *
from funcs import centerText
from funcs import posOffset as po
import inout

interface = spi(port=dispPort, device=dispDev, gpio_DC=dispDC, gpio_RST=dispRST)
disp = pcd8544(serial_interface=interface)
disp.capabilities(dispWidth, dispHeight, dispRotation)
disp.contrast(dispContrast)
disp.clear()

wiringpi.wiringPiSetupGpio()
wiringpi.pullUpDnControl(5, 1)
wiringpi.pullUpDnControl(6, 1)
backlight = inout.togglePin(dispBL)
backlight.on()

bSelect = inout.buttonPoller(buttSelect)
bMenu = inout.buttonPoller(buttMenu)
bUp = inout.buttonPoller(buttUp)
bDown = inout.buttonPoller(buttDown)
bLeft = inout.buttonPoller(buttLeft)
bRight = inout.buttonPoller(buttRight)

font = ImageFont.truetype(fontFile, fontSize)

appList = [apps.piInfo(), apps.clock()]
currentPage = 1

def menuNext():
	global currentPage
	if currentPage + 1 == len(appList):
		currentPage = 0
	else:
		currentPage += 1

def menuPrev():
	global currentPage
	if currentPage - 1 < 0:
		currentPage = len(appList) - 1
	else:
		currentPage -= 1

bLeft.callbacks["pressCall"] = menuPrev
bRight.callbacks["pressCall"] = menuNext
bMenu.callbacks["holdCall"] = backlight.toggle

while True:
	with canvas(disp) as draw:
		draw.rectangle(disp.bounding_box, outline="white")
		draw.rectangle((0, dispHeight, dispWidth, dispHeight - 8), outline="white", fill="white")
		centerText(draw, po(0,40)[1], "{}/{}".format(currentPage+1, len(appList)), "black", font)
		appList[currentPage].render(draw, font)
	sleep(0.25)
