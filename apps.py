import psutil
import socket
from datetime import datetime
import pytz
from gpiozero import CPUTemperature
import time
import ifcfg
from luma.core.render import canvas


from funcs import centerText
from funcs import posOffset as po

from config import hostname, timezone

class piInfo:
	def __init__(self, dispObj, globalVar, font, buttonPool):
		self.name = "piInfo"
		self.renderDelay = 0.25

		self.display = dispObj
		self.globalVar = globalVar
		self.font = font
		self.buttonPool = buttonPool

		self.CPUTemp = CPUTemperature()
		self.CPUFreq = CPUTemperature(sensor_file="/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq")
		pass

	def render(self, canvas):
		canvas.text(po(2,0), hostname, fill="white", font=self.font)
		canvas.text(po(2,6), socket.gethostbyname(hostname), fill="white", font=self.font)
		canvas.text(po(2,12), "CPU Usage: {}%".format(psutil.cpu_percent()), fill="white", font=self.font)
		canvas.text(po(2,18), "RAM Usage: {}%".format(psutil.virtual_memory()[2]), fill="white", font=self.font)
		canvas.text(po(2,24), "CPU Freq: {}MHz".format(int(self.CPUFreq.temperature)), fill="white", font=self.font)
		canvas.text(po(2,30), "CPU Temp: {}°C".format(round(self.CPUTemp.temperature, 2)), fill="white", font=self.font)
		time.sleep(0.25)


class clock:
	def __init__(self, dispObj, globalVar, font, buttonPool):
		self.name = "Clock"
		self.renderDelay = None

		self.display = dispObj
		self.globalVar = globalVar
		self.font = font
		self.buttonPool = buttonPool


	def render(self, canvas):
		centerText(canvas, po(0, 4)[1], datetime.now(pytz.timezone(timezone)).strftime("%H:%M:%S"), "white", self.font)
		centerText(canvas, po(0, 10)[1], datetime.now(pytz.timezone(timezone)).strftime("%A"), "white", self.font)
		centerText(canvas, po(0, 16)[1], datetime.now(pytz.timezone(timezone)).strftime("%d %B"), "white", self.font)
		centerText(canvas, po(0, 22)[1], datetime.now(pytz.timezone(timezone)).strftime("%Y"), "white", self.font)


class netInfo:
	def __init__(self, dispObj, globalVar, font, buttonPool):
		self.name = "netInfo"
		self.renderDelay = 0.5
		self.keybinds = {
			"menu": {"pressCall": self.leaveApp},

		}

		self.display = dispObj
		self.globalVar = globalVar
		self.font = font
		self.buttonPool = buttonPool


		self.appJoined = False

		self.updateIfcfg()

	def render(self, canvas):
		canvas.text(po(2,0), hostname, fill="white", font=self.font)
		canvas.text(po(2,6), self.hostInterface, fill="white", font=self.font)
		canvas.text(po(2,12), self.interfaces[self.hostInterface]["inet"], fill="white", font=self.font)

	def internalRender(self):
		while self.appJoined:
			with canvas(self.display) as draw:
				draw.text(po(2,5), "AppLoaded!", fill="white", font=self.font)
				time.sleep(0.3)

	def joinApp(self):
		self.appJoined = True
		self.buttonPool.clearCallbacks()
		self.buttonPool.update(self.keybinds)
		print(self.buttonPool._buttonPoller__originalCalls)
		self.internalRender()

	def leaveApp(self):
		self.buttonPool.resetCallbacks()
		self.appJoined = False

	def updateIfcfg(self):
		self.interfaces = ifcfg.interfaces()
		if len(self.interfaces) == 1:
			self.hostInterface = list(self.interfaces.keys())[0]
		else:
			for i in self.interfaces:
				if self.interfaces[i]["inet"] == socket.gethostbyname(hostname):
					self.hostInterface = i




appList = [piInfo, netInfo, clock]