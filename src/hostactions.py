from pinger import Pinger
import sys
import json
import threading
import logging
import datetime
import concurrent.futures

def worker_ping_host(ip):
	logging.info("Starting worker thread to ping {}".format(ip))
	pinger = Pinger(ip=ip)
	with open('activity.log', 'w+') as file:
		while 1 ==1:
			host_status = pinger.isHostAlive()
			status = '"{}", "{}"\n'.format(datetime.datetime.now().timestamp(), host_status)
			logging.info(status)
			file.write(status)
			file.flush()


if __name__ == '__main__':
	logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO)

	ip_list = [
		'172.16.10.106'
	]

	for ip in ip_list:
		worker_ping_host(ip)





