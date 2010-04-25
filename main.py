import sys
import os
import optparse
import yaml

import tornado.httpserver
import tornado.ioloop
import tornado.web

import toffee

class listen_context(object):

	def __init__(self, server, port, config):
		self.server = server
		self.port = port
		self.config = config
		self.setuid = None
		if os.getuid() == 0:
			if not config.get('uid'):
				print >> sys.stderr, 'cowardly refusing to run as root'
				sys.exit(1)
			self.setuid = config['uid']

	def __enter__(self):
		self.server.listen(port)
		if self.setuid:
			os.setuid(self.setuid)

	def __exit__(self, exc_type, exc_value, exc_traceback):
		return

if __name__ == '__main__':
	parser = optparse.OptionParser()
	parser.add_option('-p', '--port', dest='port', default=0, type='int', help='the port to listen on')
	parser.add_option('-c', '--config', dest='config', default='config.yaml', help='Configuration file to use')
	opts, args = parser.parse_args()

	settings = {}
	if os.path.exists(opts.config):
		config = yaml.load(open(opts.config))
	else:
		print >> sys.stderr, 'no config file specified (or path did not exist), exiting'
		sys.exit(1)

	settings.update(config)
	application = tornado.web.Application(toffee.routes, **settings)

	if opts.port:
		port = opts.port
	else:
		port = settings.get('port', 8080)

	server = tornado.httpserver.HTTPServer(application)
	with listen_context(server, opts.port, config):
		tornado.ioloop.IOLoop.instance().start()
