# -*- coding: utf-8 -*-
import subprocess
from webodt.converters import ODFConverter
from webodt import Document
from webodt.conf import WEBODT_ABIWORD_COMMAND

WEBODT_ABIWORD_COMMAND = ['/usr/bin/abiword', '--plugin', 'AbiCommand']

class AbiwordODFConverter(ODFConverter):


    def convert(self, document, format=None, output_filename=None, delete_on_close=True):
        output_filename, format = self._guess_format_and_filename(output_filename, format)
        process = subprocess.Popen(WEBODT_ABIWORD_COMMAND,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        args = (document.name, output_filename, format)
        process.communicate('convert %s %s %s' % args)
        fd = Document(output_filename, mode='r', delete_on_close=delete_on_close)
        return fd
