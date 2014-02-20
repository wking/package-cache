# Copyright

"A caching proxy for package downloads"

import codecs as _codecs
from distutils.core import setup
import os.path as _os_path

from package_cache import __version__


_this_dir = _os_path.dirname(__file__)


setup(
    name='package-cache',
    version=__version__,
    maintainer='W. Trevor King',
    maintainer_email='wking@tremily.us',
    url='http://blog.tremily.us/posts/package-cache/',
    download_url='https://github.com/wking/package-cache/archive/v{}.tar.gz'.format(__version__),
    license='GNU General Public License (GPL)',
    platforms=['all'],
    description=__doc__,
    long_description=_codecs.open(
        _os_path.join(_this_dir, 'README'), 'r', encoding='utf-8').read(),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: Proxy Servers',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: System :: Software Distribution',
        ],
    packages=['package_cache'],
    scripts=['package-cache.py'],
    provides=['package_cache'],
    )
