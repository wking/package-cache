# Copyright

import argparse as _argparse
import logging as _logging
import wsgiref.simple_server as _wsgiref_simple_server

from . import __version__
from . import server as _server


LOG = _logging.getLogger(__name__)


def run(*args, **kwargs):
    """Run the package-cache server using Python's WSGI reference server
    """
    parser = _argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--version', action='version',
        version='%(prog)s {}'.format(__version__))
    parser.add_argument(
        '--host', metavar='HOSTNAME', default='localhost',
        help='Host to listen as')
    parser.add_argument(
        '--port', metavar='INT', default=4000, type=int,
        help='Port to listen to')
    parser.add_argument(
        '--source', metavar='URL', action='append',
        help='URL for an upstream mirror')
    parser.add_argument(
        '--cache', metavar='PATH', default='/tmp/package-cache',
        help='Path to the package cache directory')

    args = parser.parse_args()

    server = _server.Server(sources=args.source or [], cache=args.cache)
    wsgi = _wsgiref_simple_server.make_server(
        host=args.host, port=args.port, app=server)
    LOG.info('serving WSGI on {}:{}'.format(args.host, args.port))
    wsgi.serve_forever()
