import logging


class Action
'''
This class defines a set of actions to execute 
whenever a host is deemed alive or dead
'''

	hostAlive = False

	def __init__(self):
		logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO)
		logging.info("Starting worker thread to ping {}".format(ip))



	def doAction(self):
		pass


	def 