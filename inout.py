import wiringpi
import threading
from time import sleep

wiringpi.wiringPiSetupGpio()

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
	def __init__(self, pinNum, pressCall = lambda : None, holdCall = lambda : None, sPressCall = lambda : None, repeatCall = lambda : None,):
		self.stateHistory = "0000000000000000"
		self.lastState = 0
		self.pinNum = pinNum
		wiringpi.pinMode(pinNum, 0)
		self.callbacks = {
			"pressCall": pressCall,
			"holdCall": holdCall,
			"sPressCall": sPressCall,
			"repeatCall": repeatCall,
		}
		self.kill = False
		self.__thread = threading.Thread(target=self.__poller,args=(self.pinNum, self.callbacks))
		self.__thread.start()

	def __del__(self):
		self.kill = True

	def __poller(self, pinNum, callbacks):
		while not self.kill:
			currentState = 0
			tempState = wiringpi.digitalRead(pinNum)
			if (self.lastState == 0) and (tempState == 1): # Detects first initial first
				self.lastState = tempState
				currentState = 1
			elif (self.lastState == 1) and (tempState == 1): # Detects If button still being pressed
				self.lastState = tempState
				currentState = 2
			elif (self.lastState == 1) and (tempState == 0): # Detects if button is no longer being pressed
				self.lastState = tempState
				currentState = 3
			else:
				currentState = 0
			self.stateHistory += str(currentState)
			if len(self.stateHistory) > 16:
				self.stateHistory = self.stateHistory[-16:]
			
			if self.stateHistory[-1] == "3":
				if self.stateHistory[-7:] == ("2"*6+"3"):
					callbacks["holdCall"]()
				else:
					callbacks["pressCall"]()
			if self.stateHistory[-1] == "2":
				callbacks["repeatCall"]()
			if self.stateHistory[-1] == "1":
				callbacks["sPressCall"]()
			sleep(0.05)