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
    Convert the template given by `template_name` and `dictionary` to a
    document in given `format`. The document (file-like object) will be
    returned.

    `format` is the filename extension. It's possible to use "odt", "pdf",
    "doc", "html" or "rtf" and probably more.

    `context_instance` is the optional parameter which should contain
    instance of the subclass of `django.template.Context`.

    `delete_on_close` defines whether the returned document should be deleted
    automatically when closed.

    `preprocessors` is a list of preprocessors overriding
    ``WEBODT_ODF_TEMPLATE_PREPROCESSORS`` settings variable.
    Suitable for ODF documents only.

    If the `template_name` ends with `.html`, template is considered as HTML
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
        cache=CacheManager, preprocessors=None, inline=None
    ):
    """
    Using same options as `render_to`, return `django.http.HttpResponse`
    object. The document is automatically removed when the last byte of the
    response is read.
    """
    mimetype = get_mimetype(format)
    content_fd = render_to(format, template_name, dictionary, context_instance,
        delete_on_close=True, cache=cache, preprocessors=preprocessors
    )
    response = HttpResponse(_ifile(content_fd), mimetype=mimetype)
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
