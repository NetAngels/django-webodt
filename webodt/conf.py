# -*- coding: utf8 -*-
from django.conf import settings
import os

WEBODT_TEMPLATE_PATH = getattr(settings, 'WEBODT_TEMPLATE_PATH', '')
WEBODT_DEFAULT_FORMAT = getattr(settings, 'WEBODT_DEFAULT_FORMAT', 'doc')
WEBODT_ABIWORD_COMMAND = getattr(settings, 'WEBODT_ABIWORD_COMMAND', ['/usr/bin/abiword', '--plugin', 'AbiCommand'])

# path/command to openoffice executable
WEBODT_OPENOFFICE_COMMAND = getattr(settings, 'WEBODT_OPENOFFICE_COMMAND', 'soffice')
# name of a PDF printer
WEBODT_OPENOFFICE_PDF_PRINTER = getattr(settings, 'WEBODT_OPENOFFICE_PDF_PRINTER', 'PDF') 
# output dir of a PDF printer (configurable in the printer)
WEBODT_OPENOFFICE_PDF_PRINTER_OUT = getattr(settings, 'WEBODT_OPENOFFICE_PDF_PRINTER_OUT', '/tmp/PDF') 

WEBODT_GOOGLEDOCS_EMAIL = getattr(settings, 'WEBODT_GOOGLEDOCS_EMAIL', None)
WEBODT_GOOGLEDOCS_PASSWORD = getattr(settings, 'WEBODT_GOOGLEDOCS_PASSWORD', None)
WEBODT_OPENOFFICE_SERVER = getattr(settings, 'WEBODT_OPENOFFICE_SERVER', ('localhost', 2002))
WEBODT_CONVERTER = getattr(settings, 'WEBODT_CONVERTER', 'webodt.converters.abiword.AbiwordODFConverter')
WEBODT_TMP_DIR = getattr(settings, 'WEBODT_TMP_DIR', None)
WEBODT_CACHE_DIR = getattr(settings, 'WEBODT_CACHE_DIR', '/tmp/webodt_cache')
WEBODT_ODF_TEMPLATE_PREPROCESSORS = getattr(settings, 'WEBODT_ODF_TEMPLATE_PREPROCESSORS', [
    'webodt.preprocessors.xmlfor_preprocessor',
    'webodt.preprocessors.unescape_templatetags_preprocessor',
])

