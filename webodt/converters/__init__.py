# -*- coding: utf-8 -*-
import tempfile
from django.utils.importlib import import_module
from webodt.conf import WEBODT_DEFAULT_FORMAT, WEBODT_CONVERTER

def converter():
    try:
        module_name, class_name = WEBODT_CONVERTER.rsplit('.', 1)
    except ValueError: # need more than 1 value to unpack
        raise ValueError(
            'WEBODT_CONVERTER %s have to be written in the form of "package.name.ClassName"' % WEBODT_CONVERTER)
    mod = import_module(module_name)
    Converter = getattr(mod, class_name)
    return Converter()


class ODFConverter(object):
    """ Base class for all built-in converter backends """

    WEBODT_DEFAULT_FORMAT = 'doc'

    def _guess_format_and_filename(self, filename, format):
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
            _, filename = tempfile.mkstemp(suffix = '.' + format)
        return filename, format
