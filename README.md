Package-cache is a simple caching proxy for package downloads.  Just
configure a list of upstream sources (with the `SOURCES` environment
variable) and point clients at the package-cache server.  The first
time a package is requested, we download that package from one of the
sources and cache it locally, while also streaming it to the client.
Future requests for that package are streamed directly from the local
cache.  This helps reduce the load on the network and source servers,
if you have a number of local clients that will repeatedly request the
same files (e.g. [Gentoo's distfiles][distfiles]).

We don't do anything fancy with [Cache-Control
headers][Cache-Control], since package source files should include the
version stamp in the filename itself (e.g. `my-package-0.1.2.tar.gz`).
Files are cached after the first request, and stored forever.  This
means that every package you've ever requested will still be there if
you need it later.  That's nice, but it will end up consuming a fair
amount of disk space.  You might want to periodically cull the cache,
using access times to see which files you are unlikely to want in the
future.

Package-cache is written in Python, and has no dependencies outside
the standard library.

[distfiles]: https://wiki.gentoo.org/wiki/Project:Infrastructure/Source_mirrors
[Cache-Control]: https://tools.ietf.org/html/rfc2616#section-14.9
