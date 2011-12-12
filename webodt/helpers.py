# -*- coding: utf8 -*-
from webodt.conf import WEBODT_DEFAULT_FORMAT, WEBODT_TMP_DIR
import mimetypes
import tempfile
import os


def get_mimetype(format):
    ext = '.%s' % format
    map = mimetypes.types_map.copy()
    map['.odt'] = 'application/vnd.oasis.opendocument.text'
    map['.rtf'] = 'text/richtext'
    mimetype = map[ext]
    return mimetype


def guess_format_and_filename(filename, format):
    """ guess format and filename of the output document

    Either format and filename or both can be undefined (None) variables.
    Function determines undefined variables on basis of file extension or
    default values. If needed, temporary file will be created and returned.

    @return: tuple of strings (filename, format)
    """
    # filename is defined, format is undefined
    if filename and '.' in filename and not format:
        format = filename.split('.')[-1]
    # format is undefined
    if not format:
        format = WEBODT_DEFAULT_FORMAT
    # filename is undefined
    if not filename:
        lowlevel_fd, filename = tempfile.mkstemp(suffix = '.' + format, dir=WEBODT_TMP_DIR)
        os.close(lowlevel_fd)
    return filename, format