# Copyright (C) 2014 W. Trevor King <wking@tremily.us>
#
# This file is part of package-cache.
#
# package-cache is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# package-cache is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# package-cache.  If not, see <http://www.gnu.org/licenses/>.

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
