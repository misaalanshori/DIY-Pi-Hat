import wiringpi

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
