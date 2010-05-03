import sys
import os
import optparse
import yaml
import sqlalchemy

import tornado.httpserver
import tornado.ioloop
import tornado.web

import toffee
import toffee.db
import toffee.uimodules

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-p', '--port', dest='port', default=0, type='int', help='the port to listen on')
    parser.add_option('-t', '--threads', dest='threads', default=4, type='int', help='how many threads to spawn')
    parser.add_option('-c', '--config', dest='config', default='config.yaml', help='Configuration file to use')
    parser.add_option('--memory', dest='memory_db', action='store_true', default=False, help='Load a SQLite database from memory')
    opts, args = parser.parse_args()

    settings = {}
    if os.path.exists(opts.config):
        config = yaml.load(open(opts.config))
    else:
        print >> sys.stderr, 'no config file specified (or path did not exist), exiting'
        sys.exit(1)
    settings.update(config)
    settings['ui_modules'] = toffee.uimodules.all_uimodules

    # Set up the database. You may pass in --memory as a command line option to
    # load an empty SQLite database into memory.
    if opts.memory_db:
        engine = sqlalchemy.create_engine('sqlite:///:memory:', echo=settings['debug'])
    else:
        engine = sqlalchemy.create_engine(settings['sqlite_db'], echo=settings['debug'])
    toffee.db.bind_engine(engine)

    application = tornado.web.Application(toffee.routes, **settings)

    if opts.port:
        port = opts.port
    else:
        port = settings.get('port', 8000)
    
    for x in xrange(opts.threads):
        server = tornado.httpserver.HTTPServer(application)
        server.listen(port + x)
    tornado.ioloop.IOLoop.instance().start()
