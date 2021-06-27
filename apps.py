import psutil
import socket
from datetime import datetime
import pytz
from funcs import centerText
from funcs import posOffset as po

from config import hostname, timezone

def piInfo(canvas, font):
	canvas.text(po(2,0), hostname, fill="white", font=font)
	canvas.text(po(2,6), socket.gethostbyname(hostname), fill="white", font=font)
	canvas.text(po(2,12), "CPU Usage: {}%".format(psutil.cpu_percent()), fill="white", font=font)
	canvas.text(po(2,18), "RAM Usage: {}%".format(psutil.virtual_memory()[2]), fill="white", font=font)
	canvas.text(po(2,24), datetime.now(pytz.timezone(timezone)).strftime("%d/%m/%Y"), fill="white", font=font)
	canvas.text(po(2,30), datetime.now(pytz.timezone(timezone)).strftime("%H:%M:%S"), fill="white", font=font)
