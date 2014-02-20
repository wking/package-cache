# Copyright

import email.utils as _email_utils
import mimetypes as _mimetypes
import os as _os
import urllib.error as _urllib_error
import urllib.parse as _urllib_parse
import urllib.request as _urllib_request

from . import __version__


class InvalidFile (ValueError):
    def __init__(self, url):
        super(InvalidFile, self).__init__('invalid file {!r}'.format(url))
        self.url = url


class Server (object):
    def __init__(self, sources, cache):
        self.sources = sources
        self.cache = cache
        self.opener = _urllib_request.build_opener()
        self.opener.addheaders = [
            ('User-agent', 'Package-cache/{}'.format(__version__)),
            ]
        if not _os.path.isdir(self.cache):
            _os.makedirs(self.cache, exist_ok=True)

    def __call__(self, environ, start_response):
        try:
            return self._serve_request(
                environ=environ, start_response=start_response)
        except InvalidFile:
            start_response('404 Not Found', [])
        except _urllib_error.HTTPError as e:
            print('{} {}'.format(e.code, e.reason))
            start_response('{} {}'.format(e.code, e.reason), [])
        return [b'']

    def _serve_request(self, environ, start_response):
        method = environ['REQUEST_METHOD']
        url = environ.get('PATH_INFO', None)
        if url is None:
            raise InvalidFile(url=url)
        parsed_url = _urllib_parse.urlparse(url)
        relative_path = parsed_url.path.lstrip('/').replace('/', _os.path.sep)
        cache_path = _os.path.join(self.cache, relative_path)
        if not _os.path.exists(path=cache_path):
            self._get_file_from_sources(url=url, path=cache_path)
        if not _os.path.isfile(path=cache_path):
            raise InvalidFile(url=url)
        return self._serve_file(
            path=cache_path, environ=environ, start_response=start_response)

    def _get_file_from_sources(self, url, path):
        for i, source in enumerate(self.sources):
            source_url = source.rstrip('/') + url
            try:
                self._get_file(url=source_url, path=path)
            except _urllib_error.HTTPError:
                if i == len(self.sources) - 1:
                    raise
            else:
                return

    def _get_file(self, url, path):
        with self.opener.open(url) as response:
            content_length = int(response.getheader('Content-Length'))
            with open(path, 'wb') as f:
                block_size = 8192
                while True:
                    data = response.read(block_size)
                    f.write(data)
                    if len(data) < block_size:
                        break

    def _serve_file(self, path, environ, start_response):
        headers = {
            'Content-Length': self._get_content_length(path=path),
            'Content-Type': self._get_content_type(path=path),
            'Last-Modified': self._get_last_modified(path=path),
            }
        f = open(path, 'rb')
        if 'wsgi.file_wrapper' in environ:
            file_iterator = environ['wsgi.file_wrapper'](f)
        else:
            file_iterator = iter(lambda: f.read(block_size), '')
        start_response('200 OK', list(headers.items()))
        return file_iterator

    def _get_content_length(self, path):
        """Content-Length value per RFC 2616

        Content-Length:
          https://tools.ietf.org/html/rfc2616#section-14.13
        """
        return str(_os.path.getsize(path))

    def _get_content_type(self, path):
        """Content-Type value per RFC 2616

        Content-Type:
          https://tools.ietf.org/html/rfc2616#section-14.17
        Media types:
          https://tools.ietf.org/html/rfc2616#section-3.7
        """
        mimetype, charset = _mimetypes.guess_type(url=path)
        if charset:
            return '{}; charset={}'.format(mimetype, charset)
        else:
            return mimetype

    def _get_last_modified(self, path):
        """Last-Modified value per RFC 2616

        Last-Modified:
          https://tools.ietf.org/html/rfc2616#section-14.29
        Date formats:
          https://tools.ietf.org/html/rfc2616#section-3.3.1
          https://tools.ietf.org/html/rfc1123#page-55
          https://tools.ietf.org/html/rfc822#section-5
        """
        mtime = _os.path.getmtime(path)
        return _email_utils.formatdate(
            timeval=mtime, localtime=False, usegmt=True)
