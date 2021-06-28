from luma.core.interface.serial import spi
from luma.lcd.device import pcd8544
from luma.core.render import canvas
from time import sleep
from PIL import ImageFont
import wiringpi
import importlib

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



font = ImageFont.truetype(fontFile, fontSize)


appList = []
currentPage = 0

def initApps():
	global appList
	appListTemp = []
	for i in apps.appList:
		appListTemp.append(i())
	appList = appListTemp
initApps()

def reloadApps():
	global apps
	apps = importlib.reload(apps)
	initApps()

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


bPool = inout.buttonPool({
	"select": inout.buttonPoller(buttSelect),
	"menu": inout.buttonPoller(buttMenu),
	"up": inout.buttonPoller(buttUp),
	"down": inout.buttonPoller(buttDown),
	"left": inout.buttonPoller(buttLeft),
	"right": inout.buttonPoller(buttRight),
})

bPool.update({
	"left": {"pressCall": menuPrev},
	"right": {"pressCall": menuNext},
	"menu": {"holdCall": backlight.toggle},
	"down": {"holdCall": reloadApps}
})

bPool.setOriginal()

def main():
	while True:
		with canvas(disp) as draw:
			draw.rectangle(disp.bounding_box, outline="white")
			draw.rectangle((0, dispHeight, dispWidth, dispHeight - 8), outline="white", fill="white")
			centerText(draw, po(0,40)[1], "{}/{}".format(currentPage+1, len(appList)), "black", font)
			appList[currentPage].render(draw, font)
		sleep(0.5)


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		exit()