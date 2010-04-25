import sys
import os
import optparse
import yaml

import tornado.httpserver
import tornado.ioloop
import tornado.web

import toffee

if __name__ == '__main__':
	parser = optparse.OptionParser()
	parser.add_option('-p', '--port', dest='port', default=0, type='int', help='the port to listen on')
	parser.add_option('-t', '--threads', dest='threads', default=4, type='int', help='how many threads to spawn')
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
		port = settings.get('port', 8000)
	
	for x in xrange(opts.threads):
		server = tornado.httpserver.HTTPServer(application)
		server.listen(port + x)
	tornado.ioloop.IOLoop.instance().start()
