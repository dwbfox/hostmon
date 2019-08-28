from . import Pinger
import logging
import datetime


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
        self.deadtimer = host['deadTimer']
        self.host = host
        logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.DEBUG)
        logging.captureWarnings(True)
        self.logger = logging.getLogger(__name__)
        self.logger.info('Settings: {}'.format(self.host.keys()))

    def register(self, observer, callback = None):
        self.logger.info('Registering class {} to observer'.format(observer.__class__.__name__))
        self.observers.append(observer)

    def unregister(self, observer):
        del self.observers[observer]

    def dispatch(self, event):
        for observer in self.observers:
            observer.update(event)

    def observe_host(self):
        pinger = Pinger.Pinger(ip=self.host['monitorIP'], frequency=str(self.host['frequency']))

        ''' REMOVE BEFORE FLIGHT
        e = Event('deadEvent', True, '0000', '00:0:00')
        self.dispatch(e)

        ### REMOVE BEFORE FLIGHT
        '''
        while True:
            host_alive = pinger.isHostAlive()
            if host_alive: self.timeoutcount = 0
            timestamp = datetime.datetime.now().timestamp()
            if self.timeoutcount >= self.deadtimer:
                e = Event('deadEvent', True, timestamp, None)
                self.dispatch(e)
                continue
            if not host_alive:
                self.timeoutcount += 1
            e = Event('pingEvent', host_alive, timestamp, None)
            self.dispatch(e)


