import logging
import subprocess
import threading
import sys
import datetime

class PingerException(Exception): pass
class Pinger:
    ip = None
    def __init__(self, **kwargs):
        self.ip = kwargs['ip']
        self.frequency = str(kwargs['frequency'])

    def isHostAlive(self):
        response = subprocess.Popen(['/bin/ping', '-c', '2', '-w', self.frequency, self.ip], stdout=subprocess.DEVNULL).wait()
        return response == 0
