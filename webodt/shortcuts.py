# -*- coding: utf8 -*-
import os

from django.http import HttpResponse
from django.template import Context
from webodt.cache import CacheManager
from webodt.converters import converter
from webodt.helpers import get_mimetype

import webodt

def render_to(format, template_name,
        dictionary=None, context_instance=None, delete_on_close=True,
        cache=CacheManager, preprocessors=None
    ):
    """
    Convert the template given by :attr:`template_name` and :attr:`dictionary`
    to a document in given :attr:`format`. The document (file-like object) will
    be returned.

    :keyword format: Filename extension. It's possible to use "odt", "pdf",
                     "doc", "html" or "rtf" and probably more.

    :keyword context_instance: Optional parameter which should contain instance
                               of the subclass of `django.template.Context`.

    :keyword delete_on_close: Flag which defines whether the returned document
                              should be deleted automatically when closed.

    :keyword preprocessors: List of preprocessors overriding :attr:`WEBODT_ODF_TEMPLATE_PREPROCESSORS`
                            settings variable.  Suitable for ODF documents only.

    If the :attr:`template_name` ends with ".html", template is considered as HTML
    template, otherwise as ODF based template.
    """
    template = _Template(template_name, preprocessors=preprocessors)
    dictionary = dictionary or {}
    if context_instance:
        context_instance.update(dictionary)
    else:
        context_instance = Context(dictionary)
    document = template.render(context_instance, delete_on_close=delete_on_close)
    if format == 'odt':
        return document
    formatted_document = None
    if cache:
        cache_mgr = cache()
        formatted_document = cache_mgr.get(document, format)
    if not formatted_document:
        formatted_document = converter().convert(document, format, delete_on_close=delete_on_close)
        cache_mgr.set(document, format, formatted_document)
    document.close()
    return formatted_document


def render_to_response(template_name,
        dictionary=None, context_instance=None, filename=None, format='odt',
        cache=CacheManager, preprocessors=None, inline=None, iterator=False,
    ):
    """
    Using same options as :func:`render_to`, return :class:`django.http.HttpResponse`
    object. The document is automatically removed after the last byte of the
    response have been read.

    :keyword iterator: is a flag which determines whether returned
                       :class:`HttpResponse` object should be initialized with
                       a string or with an iterator.

    Consider using iterator if you tend to send large documents only, otherwise
    set this flag to :const:`False`. Be aware that some middlewares can "eat"
    your iterator-based HTTP responses. See `Ticket #6527
    <https://code.djangoproject.com/ticket/6527>`_ for more details.
    """
    mimetype = get_mimetype(format)
    content_fd = render_to(format, template_name, dictionary, context_instance,
        delete_on_close=True, cache=cache, preprocessors=preprocessors
    )
    if iterator:
        content = _ifile(content_fd)
    else:
        content = content_fd.read()
    response = HttpResponse(content, mimetype=mimetype)
    if not filename:
        filename = os.path.basename(template_name)
        filename += '.%s' % format
    response['Content-Disposition'] = (
        inline and 'inline' or 'attachment; filename="%s"' % filename
    )
    return response


def _Template(template_name, preprocessors):
    if template_name.endswith('.html'):
        return webodt.HTMLTemplate(template_name)
    return webodt.ODFTemplate(template_name, preprocessors=preprocessors)


def _ifile(fd, chunk_size=1024, close_on_exit=True):
    while True:
        data = fd.read(chunk_size)
        if not data:
            if close_on_exit:
                fd.close()
            break
        else:
            yield data
