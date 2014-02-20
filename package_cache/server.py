# Copyright

import email.utils as _email_utils
import mimetypes as _mimetypes
import os as _os
import urllib.parse as _urllib_parse


class InvalidFile (ValueError):
    def __init__(self, url):
        super(InvalidFile, self).__init__('invalid file {!r}'.format(url))
        self.url = url


class Server (object):
    def __init__(self, sources, cache):
        self.sources = sources
        self.cache = cache

    def __call__(self, environ, start_response):
        try:
            return self._serve_request(
                environ=environ, start_response=start_response)
        except InvalidFile:
            start_response(status='404 Not Found', response_headers=[])

    def _serve_request(self, environ, start_response):
        method = environ['REQUEST_METHOD']
        url = environ.get('PATH_INFO', None)
        if url is None:
            raise InvalidFile(url=url)
        parsed_url = _urllib_parse.urlparse(urlstring=url)
        relative_path = parsed_url.path.lstrip('/').replace('/', _os.path.sep)
        cache_path = _os.path.join(self.cache, relative_path)
        if not _os.path.exists(path=cache_path):
            self._get_file(url=url, path=cache_path)
        if not _os.path.isfile(path=cache_path):
            raise InvalidFile(url=url)
        return self._serve_file(
            path=cache_path, environ=environ, start_response=start_response)

    def _get_file(self, url, path):
        raise NotImplementedError()

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
        start_response(
            status='200 OK',
            response_headers=list(headers.items()))
        return file_iterator

    def _get_content_length(self, path):
        """Content-Length value per RFC 2616

        Content-Length:
          https://tools.ietf.org/html/rfc2616#section-14.13
        """
        return str(_os.path.getsize(path=path))

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
        mtime = _os.path.getmtime(path=path)
        return _email_utils.formatdate(
            timeval=mtime, localtime=False, usegmt=True)
