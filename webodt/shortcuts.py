# -*- coding: utf8 -*-
import os
import mimetypes

from django.http import HttpResponse
from django.template import Context
from webodt.cache import CacheManager
from webodt.converters import converter

import webodt

def render_to(format, template_name, dictionary=None, context_instance=None, delete_on_close=True,
              cache=CacheManager):
    template = webodt.ODFTemplate(template_name)
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
        dictionary=None, context_instance=None, filename=None, format='odt', cache=CacheManager):
    mimetype = _get_mimetype(format)
    content_fd = render_to(format, template_name, dictionary, context_instance,
                           delete_on_close=True, cache=cache)
    response = HttpResponse(_ifile(content_fd), mimetype=mimetype)
    if not filename:
        filename = os.path.basename(template_name)
        filename += '.%s' % format
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    return response


def _ifile(fd, chunk_size=1024, close_on_exit=True):
    while True:
        data = fd.read(chunk_size)
        if not data:
            if close_on_exit:
                fd.close()
            break
        else:
            yield data


def _get_mimetype(format):
    ext = '.%s' % format
    map = mimetypes.types_map.copy()
    map['.odt'] = 'application/vnd.oasis.opendocument.text'
    map['.rtf'] = 'text/richtext'
    mimetype = map[ext]
    return mimetype
