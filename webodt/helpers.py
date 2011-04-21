# -*- coding: utf8 -*-
import mimetypes


def get_mimetype(format):
    ext = '.%s' % format
    map = mimetypes.types_map.copy()
    map['.odt'] = 'application/vnd.oasis.opendocument.text'
    map['.rtf'] = 'text/richtext'
    mimetype = map[ext]
    return mimetype