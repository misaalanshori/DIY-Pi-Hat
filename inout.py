from types import BuiltinFunctionType
import wiringpi
import threading
from time import sleep
import funcs
import copy

wiringpi.wiringPiSetupGpio()

# Class for pins to be toggled
class togglePin:
    def __init__(self, pinNum):
        self.pinNum = pinNum
        self.state = False
        wiringpi.pinMode(pinNum, 1)
        wiringpi.digitalWrite(pinNum, 0)
    def on(self):
        wiringpi.digitalWrite(self.pinNum, 1)
        self.state = True
    def off(self):
        wiringpi.digitalWrite(self.pinNum, 0)
        self.state = False
    def toggle(self):
        self.state = not self.state
        wiringpi.digitalWrite(self.pinNum, self.state)
    
class buttonPoller:
    def __init__(self, buttons = {}):
        self.buttons = buttons
        self.paused = {}
        self.callbacks = {}
        self.killThread = False
        self.callbackBuffer = []
        self.mainLoopCallbackBuffer = []
        # self.__callbackWaiter = threading.Event()
        for button in buttons:
            self.callbacks[button] = {}
            for calls in buttons[button].callbacks:
                self.callbacks[button][calls] = buttons[button].callbacks[calls]
        self.__originalCalls = {**self.callbacks.copy()}

        self.__threadDelay = 0.05

        self.__thread = threading.Thread(target=self.__poller)
        self.__callbackThread = threading.Thread(target=self.__callbackBufferThread)
        self.__thread.start()
        self.__callbackThread.start()
        
    def update(self, callbacks):
        self.callbacks = funcs.badDeepCopy(callbacks)
        for button in self.callbacks:
            for calls in self.callbacks[button]:
                self.buttons[button].callbacks[calls] = self.callbacks[button][calls]

    def clearCallbacks(self):
        for button in self.callbacks:
            for calls in self.callbacks[button]:
                self.callbacks[button][calls] = lambda : None
        self.update(funcs.badDeepCopy(self.callbacks))



    def setOriginal(self):
        print("original Set!")
        self.__originalCalls = funcs.badDeepCopy(self.callbacks)

    def resetCallbacks(self):
        print("callback reset")
        print(self.__originalCalls)
        self.update(self.__originalCalls)

    def pausePoller(self, buttName):
        self.paused[buttName] = self.buttons.pop(buttName)        

    def pauseAll(self):
        self.paused = {**self.paused, **self.buttons}
        self.buttons = {}


    def resumePoller(self, buttName):
        self.buttons[buttName] = self.resume.pop(buttName)

    def resumeAll(self):
        self.buttons = {**self.buttons, **self.paused}
        self.paused = {}

    def __poller(self):
        while not self.killThread:
            for button in self.buttons:
                butt = self.buttons[button]
                currentState = 0
                tempState = wiringpi.digitalRead(butt.pinNum)
                if (butt.lastState == 0) and (tempState == 1): # Detects first initial press
                    butt.lastState = tempState
                    currentState = 1
                elif (butt.lastState == 1) and (tempState == 1): # Detects If button still being pressed
                    butt.lastState = tempState
                    currentState = 2
                elif (butt.lastState == 1) and (tempState == 0): # Detects if button is no longer being pressed
                    butt.lastState = tempState
                    currentState = 3
                else:
                    currentState = 0

                butt.stateHistory += str(currentState)
                butt.stateHistory = butt.stateHistory[-64:]
                
                if butt.stateHistory[-1] == "3":
                    if butt.stateHistory[-7:] == ("2"*6+"3"): #0.02 -> 15
                        self.callbackBuffer.append(butt.callbacks["holdCall"])
                    else:
                        self.callbackBuffer.append(butt.callbacks["pressCall"])

                if butt.stateHistory[-1] == "2":
                    self.callbackBuffer.append(butt.callbacks["repeatCall"])

                if butt.stateHistory[-1] == "1":
                    self.callbackBuffer.append(butt.callbacks["sPressCall"])
                
            # if self.callbackBuffer != set():
            #     self.__callbackWaiter.set()
            sleep(self.__threadDelay)
            

    def __callbackBufferThread(self):
        while not self.killThread:
            # self.__callbackWaiter.wait()
            # self.__callbackWaiter.clear()
            tempCalls = self.callbackBuffer.copy()
            self.callbackBuffer.clear()
            for call in tempCalls:
                if type(call) == list:
                    for futureCall in call:
                        print("adding to mainloop buffer")
                        print(futureCall)
                        self.mainLoopCallbackBuffer.append(futureCall)
                        print(self.mainLoopCallbackBuffer)
                        print("="*8)
                else:
                    call()
            sleep(0.05)





class buttonClass:
    def __init__(self, pinNum, pinMode = 0 , pressCall = lambda : None, holdCall = lambda : None, sPressCall = lambda : None, repeatCall = lambda : None,):
        self.stateHistory = "0"*64
        self.lastState = 0
        self.pinNum = pinNum
        self.callbacks = {
            "pressCall": pressCall,
            "holdCall": holdCall,
            "sPressCall": sPressCall,
            "repeatCall": repeatCall,
        }
        wiringpi.pinMode(pinNum, pinMode)
        wiringpi.pullUpDnControl(pinNum, wiringpi.GPIO.PUD_DOWN)

    def setWiringPiCallback(self, callb):
        wiringpi.wiringPiISR(self.pinNum, wiringpi.GPIO.INT_EDGE_RISING, callb)

    def debug(self):
        def pCall(self):
            print(self.pinNum + " Pressed")
        def hCall(self):
            print(self.pinNum + " Held")
        def sPCall(self):
            print(self.pinNum + " SPressed")
        def rCall(self):
            print(self.pinNum + " Repeat")
        

        self.__callbackOG = self.callbacks
        self.callbacks = {
            "pressCall": pCall,
            "holdCall": hCall,
            "sPressCall": sPCall,
            "repeatCall": rCall,
        }
    
    def debugOff(self):
        self.callbacks = self.__callbackOG
