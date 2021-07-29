# Import required libraries
from luma.core.interface.serial import spi
from luma.lcd.device import pcd8544
from luma.core.render import canvas
from time import sleep
from PIL import ImageFont
import wiringpi
import importlib

#Import other python files
import apps
from config import *
from funcs import centerText
from funcs import posOffset as po
import inout

# Configure Display
interface = spi(port=dispPort, device=dispDev, gpio_DC=dispDC, gpio_RST=dispRST)
disp = pcd8544(serial_interface=interface)
disp.capabilities(dispWidth, dispHeight, dispRotation)
disp.contrast(dispContrast)
disp.clear()

# Setup wiringpi
wiringpi.wiringPiSetupGpio()
wiringpi.pullUpDnControl(5, 1) # Set some pulldowns
wiringpi.pullUpDnControl(6, 1)
backlight = inout.togglePin(dispBL) # Configure Backlight
backlight.on()



font = ImageFont.truetype(fontFile, fontSize)

# Array and int to store the appClasses and keep track of the current app
appList = []
currentPage = 0

# Global variables to get passed on to the apps
gVariables = {
    "gSDelay": 0.033
}


# mainLoopCallbacks = set()

# Initialize the apps inside the app list
def initApps():
    global appList
    appListTemp = []
    for i in apps.appList:
        appListTemp.append(i(disp, gVariables, font, bPool))
    appList = appListTemp

# Reload the apps code and re-init the apps
def reloadApps():
    global apps
    apps = importlib.reload(apps)
    initApps()

# Move the menu position
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

# Calls the joinApp method of current app to load the internal app render
def joinApp():
    appList[currentPage].joinApp()

# Initialize the buttonPooler with the button pins
bPool = inout.buttonPoller({
    "select": inout.buttonClass(buttSelect),
    "menu": inout.buttonClass(buttMenu),
    "up": inout.buttonClass(buttUp),
    "down": inout.buttonClass(buttDown),
    "left": inout.buttonClass(buttLeft),
    "right": inout.buttonClass(buttRight),
})

# Update the buttons with the callbacks functions
bPool.update({
    "left": {"pressCall": menuPrev},
    "right": {"pressCall": menuNext},
    "menu": {"holdCall": backlight.toggle},
    "down": {"holdCall": reloadApps},
    "select": {"pressCall": [joinApp]},
})

bPool.setOriginal() # Set the current callbacks as Original so it can be reset later



def main():
    # Init apps and start the main loop
    initApps()
    while True:
        tempCalls = bPool.mainLoopCallbackBuffer.copy()
        bPool.mainLoopCallbackBuffer.clear()
        for call in tempCalls:
            print("calling from mainloop")
            print(call)
            print("="*8)
            call()
        with canvas(disp) as draw:
            draw.rectangle(disp.bounding_box, outline="white")
            draw.rectangle((0, dispHeight, dispWidth, dispHeight - 8), outline="white", fill="white")
            centerText(draw, po(0,40)[1], "{}/{}".format(currentPage+1, len(appList)), "black", font)

            appList[currentPage].render(draw)

        sleep(appList[currentPage].renderDelay or gVariables["gSDelay"])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()