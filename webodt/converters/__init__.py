# -*- coding: utf-8 -*-
import os
import tempfile
from django.utils.importlib import import_module
from webodt.conf import WEBODT_DEFAULT_FORMAT, WEBODT_CONVERTER, WEBODT_TMP_DIR

def converter():
    """ Create and return Converter instance
    on a basis of ``WEBODT_CONVERTER`` settings variable
    """
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

    def convert(self, document, format=None, output_filename=None, delete_on_close=True):
        """ convert document and return file-like object representing output
        document """
        if format == 'odt':
            return document
        raise NotImplementedError("Should be implemented in subclass")


class ConverterError(Exception):
    pass
