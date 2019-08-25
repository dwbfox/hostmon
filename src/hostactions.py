from hostactions import Pinger
from hostactions.Observable import Observable
from hostactions.plugins.PingObserver import PingObserver
import json
import logging
logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO)
logging.captureWarnings(True)
logger = logging.getLogger(__name__)

def get_settings(filename='settings.json'):
	settingsJson = None
	with open(filename, 'r') as file:
		settingsJson = json.load(file)
	return settingsJson


if __name__ == '__main__':
	logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO)

	# load host and ping settings
	settings = get_settings()
	logging.info('Settings: {}'.format(settings))
	if settings == None: raise Exception('No settings loaded.')

	# spawn worker threads to begin polling hosts
	# and emit events on each response]
	# @todo -- move this into its own python thread
	for host in settings['hosts']:
		logger.info(host)
		pub = Observable(host)
		pub.observe_host()
		pingObserver = PingObserver('pinghandler', pub)
