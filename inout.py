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
	def __init__(self, pinNum, pinMode = 0 , pressCall = lambda : None, holdCall = lambda : None, sPressCall = lambda : None, repeatCall = lambda : None,):
		self.stateHistory = "0000000000000000"
		self.lastState = 0
		self.pinNum = pinNum
		self.callbacks = {
			"pressCall": pressCall,
			"holdCall": holdCall,
			"sPressCall": sPressCall,
			"repeatCall": repeatCall,
		}
		self.kill = False

		wiringpi.pinMode(pinNum, pinMode)
		self.__thread = threading.Thread(target=self.__poller)
		self.__thread.start()

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

	def __del__(self):
		self.kill = True

	def __poller(self):
		while not self.kill:
			currentState = 0
			tempState = wiringpi.digitalRead(self.pinNum)
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
			self.stateHistory = self.stateHistory[-16:]
			
			if self.stateHistory[-1] == "3":
				if self.stateHistory[-4:] == ("2"*3+"3"):
					self.callbacks["holdCall"]()
				else:
					self.callbacks["pressCall"]()

			if self.stateHistory[-1] == "2":
				self.callbacks["repeatCall"]()

			if self.stateHistory[-1] == "1":
				self.callbacks["sPressCall"]()

			sleep(0.1)