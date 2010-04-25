import os
import optparse
import yaml

import tornado.httpserver
import tornado.ioloop
import tornado.web

import toffee


if __name__ == '__main__':
	defaultport = 80 if os.geteuid() == 0 else 8888
	parser = optparse.OptionParser()
	parser.add_option('-p', '--port', dest='port', default=defaultport, help='the port to listen on')
	parser.add_option('-c', '--config', dest='config', default='config.yaml', help='Configuration file to use')
	opts, args = parser.parse_args()

	settings = {}
	if os.path.exists(opts.config):
		settings.update(yaml.load(open(opts.config)))
		application = tornado.web.Application(toffee.routes, **settings)

	server = tornado.httpserver.HTTPServer(application)
	server.listen(opts.port)
	tornado.ioloop.IOLoop.instance().start()
