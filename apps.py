import psutil
import socket
from datetime import datetime
import pytz
from gpiozero import CPUTemperature

from funcs import centerText
from funcs import posOffset as po

from config import hostname, timezone

class piInfo:
	def __init__(self):
		self.name = "piInfo"

		self.CPUTemp = CPUTemperature()
		self.CPUFreq = CPUTemperature(sensor_file="/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq")
		pass

	def render(self, canvas, font):
		canvas.text(po(2,0), hostname, fill="white", font=font)
		canvas.text(po(2,6), socket.gethostbyname(hostname), fill="white", font=font)
		canvas.text(po(2,12), "CPU Usage: {}%".format(psutil.cpu_percent()), fill="white", font=font)
		canvas.text(po(2,18), "RAM Usage: {}%".format(psutil.virtual_memory()[2]), fill="white", font=font)
		canvas.text(po(2,24), "CPU Freq: {}MHz".format(int(self.CPUFreq.temperature)), fill="white", font=font)
		canvas.text(po(2,30), "CPU Temp: {}°C".format(round(self.CPUTemp.temperature, 2)), fill="white", font=font)


class clock:
	def __init__(self):
		self.name = "Clock"

	def render(self, canvas, font):
		centerText(canvas, po(0, 4)[1], datetime.now(pytz.timezone(timezone)).strftime("%H:%M:%S"), "white", font)
		centerText(canvas, po(0, 10)[1], datetime.now(pytz.timezone(timezone)).strftime("%A"), "white", font)
		centerText(canvas, po(0, 16)[1], datetime.now(pytz.timezone(timezone)).strftime("%d %B"), "white", font)
		centerText(canvas, po(0, 22)[1], datetime.now(pytz.timezone(timezone)).strftime("%Y"), "white", font)


appList = [piInfo, clock]