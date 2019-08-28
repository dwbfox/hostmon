from dracclient import client
import logging
import subprocess
import time
import urllib3

logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO)
logging.captureWarnings(True)
logger = logging.getLogger('PingObserver')

class PingObserver:

    def __init__(self, name, observable, host):
        logger.info('Initialized observer')
        observable.register(self)
        self.poweronoff_cooldown_time = 30
        self.alreadyDead = False
        self.alreadyAlive = True
        self.host = host
        urllib3.disable_warnings()
        self._dracclient = client.DRACClient(self.host['bmc']['ip'], 'root', 'calvin') #please don't do this

    def _turn_host_on(self):
        if self._is_dry_run():
            logger.info('DRY RUN -- simulated power on')
            return
        logger.info('Host offline: {}'.format(self._is_host_off() ) )
        logger.info('Powering on {}'.format(self.host['bmc']['ip']) )
        self._dracclient.set_power_state('POWER_ON')


    def _is_dry_run(self):
        return self.host['dryrun']

    def _is_host_off(self):
        return ('POWER_OFF' == self._dracclient.get_power_state())

    def _turn_host_off_bmc(self):
        if self._is_dry_run():
            logger.info('DRY RUN -- simulated power off')
            return
        logger.info('Powering off {}'.format(self.host['bmc']['ip'])  )
        self._dracclient.set_power_state('POWER_OFF')


    def _turn_host_off(self):
        if self._is_dry_run():
            logger.info('DRY RUN -- simulated power off')
            return
        response = subprocess.Popen(['/usr/bin/ssh', '-i', '/home/jupiter/.ssh/europa_lab', 'root@{}'.format(self.host['monitorIP']), 'shutdown -h now'],  stdout=subprocess.DEVNULL).wait()
        time.sleep(10)
        if not self._is_host_off():
            logger.warn('Graceful shutdown seems to have failed, falling back to BMC shutdown...')
            self._turn_host_off_bmc()


    def _mark_subject_alive(self):
        self.alreadyAlive = True
        self.alreadyDead = False

    def _mark_subject_dead(self):
        self.alreadyAlive = False
        self.alreadyDead = True

    def update(self, event):
        logger.info('{} {}'.format(self.host['bmc']['ip'], str(event)) )

        # Host is already dead
        if event.assertion and event.name == 'pingEvent' and self.alreadyDead:
            if self.alreadyAlive:
                logger.info('Subject is already alive...skipping')
                return
            logger.info('Subject just came back online! Turning servers back on!')
            self._turn_host_on()
            self._mark_subject_alive()
            logger.info('Turned host on/off, cooling down for {} seconds'.format(self.poweronoff_cooldown_time))
            time.sleep(self.poweronoff_cooldown_time)

        # Host is alive and well
        if event.assertion and event.name == 'pingEvent':
            logger.info('Subject has been alive...doing nothing')


        # Host has gone dead
        if event.assertion and event.name == 'deadEvent':
            if self.alreadyDead:
                logger.info('Subject is already dead...skipping')
                return
            self._mark_subject_dead()
            if self._is_host_off():
                logger.info('Host is already offline...')
                return
            logger.info('Subject has dropped off, shutting down non-essential servers....')
            self._turn_host_off()
            logger.info('Turned host on/off, cooling down for {} seconds'.format(self.poweronoff_cooldown_time))
            time.sleep(self.poweronoff_cooldown_time)
            

