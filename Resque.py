#!/usr/bin/env python

import re
import commands

RESQUE_TOTAL_PROCESSED = "redis-cli --raw get resque:stat:processed"
RESQUE_TOTAL_FAILED = "redis-cli --raw get resque:stat:failed"

RESQUE_QUEUES = "redis-cli --raw smembers resque:queues"

class Resque:
	def __init__(self, agent_config, checks_logger, raw_config):
		self.agent_config = agent_config
		self.checks_logger = checks_logger
		self.raw_config = raw_config
	
	def run(self):
		stats = {}
		stats['total_processed'] = int(commands.getoutput(RESQUE_TOTAL_PROCESSED))
		stats['total_failed'] = int(commands.getoutput(RESQUE_TOTAL_FAILED))
		stats['total_pending'] = 0
		for queue in commands.getoutput(RESQUE_QUEUES).splitlines():
			stats[queue] = int(commands.getoutput("redis-cli --raw llen resque:queue:"+queue))
			stats['total_pending'] = stats['total_pending']+stats[queue]
		return stats

if __name__ == '__main__':
	resque = Resque(None, None, None)
	print resque.run()
