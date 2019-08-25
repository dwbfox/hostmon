from awake import wol
from dracclient import client
import logging
import subprocess
import time
import urllib3

logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO)
logging.captureWarnings(True)
logger = logging.getLogger('PingObserver')

class PingObserver:

    def __init__(self, name, observable):
        logger.info('Initialized observer')
        observable.register(self)
        self.host_ip = '172.16.10.2'
        self.drac_ip = '172.16.10.132'
        self.poweronoff_cooldown_time = 30
        self.alreadyDead = False
        self.alreadyAlive = True
        urllib3.disable_warnings()
        self._dracclient = client.DRACClient(self.drac_ip, 'root', 'calvin') #please don't do this

    def _turn_host_on(self):
        logger.info('Host offline: {}'.format(self._is_host_off() ) )
        logger.info('Powering on {}'.format(self.drac_ip) )
        self._dracclient.set_power_state('POWER_ON')


    def _is_host_off(self):
        return ('POWER_OFF' == self._dracclient.get_power_state())


    def _turn_host_off_bmc(self):
        '''Use the out of band management
        system to turn off the host'''
        logger.info('Powering off {}'.format(self.drac_ip) )
        self._dracclient.set_power_state('POWER_OFF')


    def _turn_host_off(self):
        response = subprocess.Popen(['/usr/bin/ssh', '-i', '/home/jupiter/.ssh/europa_lab', 'root@{}'.format(self.host_ip), 'shutdown -h now'],  stdout=subprocess.DEVNULL).wait()
        if not response or not self._is_host_off():
            logger.warn('Graceful shutdown seems to have failed, falling back to BMC shutdown...')
            self._turn_host_off_bmc()
        logger.debug(response)


    def _mark_subject_alive(self):
        self.alreadyAlive = True
        self.alreadyDead = False

    def _mark_subject_dead(self):
        self.alreadyAlive = False
        self.alreadyDead = True

    def update(self, event):
        logger.info(str(event))
        if event.assertion and event.name == 'pingEvent' and self.alreadyDead:
            if self.alreadyAlive:
                logger.info('Subject is already alive...skdrac_ipping')
                return
            logger.info('Subject just came back online! Turning servers back on!')
            self._turn_host_on()
            self._mark_subject_alive()
            logger.info('Turned host on/off, cooling down for {} seconds'.format(self.poweronoff_cooldown_time))
            time.sleep(self.poweronoff_cooldown_time)
        if event.assertion and event.name == 'pingEvent':
            logger.info('Subject has been alive...doing nothing')

        if event.assertion and event.name == 'deadEvent':
            if self.alreadyDead:
                logger.info('Subject is already dead...skipping')
                return
            logger.info('Subject has dropped off, shutting down non-essential servers....')
            self._turn_host_off()
            self._mark_subject_dead()
            logger.info('Turned host on/off, cooling down for {} seconds'.format(self.poweronoff_cooldown_time))
            time.sleep(self.poweronoff_cooldown_time)
            

