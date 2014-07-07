# -*- coding: utf-8 -*-
"""Query providers for metadata."""

from .registry import services
from ._core import EAN13
from ._exceptions import NotRecognizedServiceError, NotValidISBNError


def query(isbn, service='default', cache='default'):
    """Query worldcat.org, Google Books (JSON API), ... for metadata."""
    from .registry import metadata_cache           # <-- dinamic now!
    ean = EAN13(isbn)
    if not ean:
        raise NotValidISBNError(isbn)
    isbn = ean
    if cache == 'default':
        cache = metadata_cache
    if service != 'default' and service not in services:
        raise NotRecognizedServiceError(service)
    if cache is None:  # pragma: no cover
        return services[service](isbn)
    key = isbn + service
    try:
        if cache[key]:
            return cache[key]
        else: 
            raise
    except:
        meta = services[service](isbn)
        if meta:
            cache[key] = meta
        return meta if meta else None
