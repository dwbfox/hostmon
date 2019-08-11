import logging
import subprocess

class PingerException(Exception): pass

class Pinger:
	ip = None
	def __init__(self, **kwargs):
		if 'ip' not in kwargs:
			raise PingerException('IP address not specified!')
		self.ip = kwargs['ip']

	def isHostAlive(self):
		response = subprocess.Popen(['/bin/ping', '-c', '2', '-w', '2', self.ip], stdout=subprocess.DEVNULL).wait()
		return response == 0
