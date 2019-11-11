#! /usr/bin/python3

import concurrent.futures
from hostactions import Pinger
from hostactions.Observable import Observable
from hostactions.plugins.PingObserver import PingObserver
import json
import logging
import threading

logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO)
logging.captureWarnings(True)
logger = logging.getLogger(__name__)


def get_settings(filename='settings.json'):
	settingsJson = None
	with open(filename, 'r') as file:
		settingsJson = json.load(file)
	return settingsJson

def initObservers(hostData):
	print('Spawning thread for {}'.format(hostData['bmc']['ip']))
	pub = Observable(hostData)
	pingObserver = PingObserver('pinghandler', pub, hostData)
	pub.observe_host()


if __name__ == '__main__':
	# load host and ping settings
	settings = get_settings()
	if settings == None: raise Exception('No settings loaded.')

	# spawn worker threads to begin polling hosts
	# and emit events on each response]
	# @todo -- move this into its own python thread
	with concurrent.futures.ThreadPoolExecutor(max_workers=settings['global']['max_workers'] as executor:
		result = executor.map(initObservers, settings['hosts'])
		for r in result:
			print(type(r))
