from . import Pinger
import logging
import datetime

logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO)
logging.captureWarnings(True)
logger = logging.getLogger(__name__)

class Event:
    def __init__(self, name, assertion, timestamp, meta):
        self.name = name
        self.assertion = assertion
        self.time = timestamp

    def __repr__(self):
        return 'Event name: {} | Event assertions: {} | Event time: {}'.format(self.name, self.assertion, self.time)


class Observable:
    def __init__(self, host):
        self.observers = []
        self.timeoutcount = 0
        self.deadtimer = 60
        self.host = host
        logger.info('Settings: {}'.format(self.host.keys()))

    def register(self, observer, callback = None):
        self.observers.append(observer)

    def unregister(self, observer):
        del self.observers[observer]

    def dispatch(self, event):
        for observer in self.observers:
            observer.update(event)

    def observe_host(self):
        pinger = Pinger.Pinger(ip=self.host['monitorIp'], frequency=str(self.host['frequency']))

        ''' REMOVE BEFORE FLIGHT
        e = Event('deadEvent', True, '0000', '00:0:00')
        self.dispatch(e)

        ### REMOVE BEFORE FLIGHT
        '''
        while True:
            host_alive = pinger.isHostAlive()
            if host_alive: self.timeoutcount = 0
            logger.info('Timeout count: {} | Dead Timer: {}'.format(self.timeoutcount, self.deadtimer))
            timestamp = datetime.datetime.now().timestamp()
            if self.timeoutcount >= self.deadtimer:
                e = Event('deadEvent', True, timestamp, mac)
                self.dispatch(e)
                continue
            if not host_alive:
                self.timeoutcount += 1
            e = Event('pingEvent', host_alive, timestamp, None)
            self.dispatch(e)


