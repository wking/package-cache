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

"A caching proxy for package downloads"

import logging as _logging


__version__ = '0.0'

LOG = _logging.getLogger(__name__)
LOG.setLevel(_logging.WARNING)
LOG.addHandler(_logging.StreamHandler())
