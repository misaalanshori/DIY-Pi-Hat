import psutil
import socket
from datetime import datetime
import pytz

hostname = "raspberrypi.local"
timezone = "Asia/Jakarta"

def piInfo(canvas, font):
	canvas.text((2,-3), hostname, fill="white", font=font)
	canvas.text((2,3), socket.gethostbyname(hostname), fill="white", font=font)
	canvas.text((2,9), "CPU Usage: {}%".format(psutil.cpu_percent()), fill="white", font=font)
	canvas.text((2,15), "RAM Usage: {}%".format(psutil.virtual_memory()[2]), fill="white", font=font)
	canvas.text((2,21), datetime.now(pytz.timezone(timezone)).strftime("%d/%m/%Y"), fill="white", font=font)
	canvas.text((2,27), datetime.now(pytz.timezone(timezone)).strftime("%H:%M:%S"), fill="white", font=font)
