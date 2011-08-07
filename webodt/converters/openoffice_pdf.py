# -*- coding: utf-8 -*-
import subprocess, os
from webodt.converters import ODFConverter
from webodt import Document
from webodt.conf import WEBODT_OPENOFFICE_COMMAND, WEBODT_OPENOFFICE_PDF_PRINTER, WEBODT_OPENOFFICE_PDF_PRINTER_OUT

class OpenOfficePDFConverter(ODFConverter):

    def convert(self, document, format=None, output_filename=None, delete_on_close=True):
        output_filename, format = self._guess_format_and_filename(output_filename, format)
        if format != 'pdf':
            raise ValueError("OpenOfficePDFConverter only supports conversion to PDF. Conversion to %s is not supported." % (format,))
        command = [WEBODT_OPENOFFICE_COMMAND] + ['-norestore', '-nofirststartwizard', '-nologo', '-headless', '-pt', WEBODT_OPENOFFICE_PDF_PRINTER, document.name ]
        process = subprocess.Popen(command,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        os.waitpid(0, 0) # works only on Unix
        #process.wait() # this here doesn't wait for end of "printing"
        filename, _old_ext = os.path.splitext(os.path.split(document.name)[1])
        new_filepath = os.path.join(WEBODT_OPENOFFICE_PDF_PRINTER_OUT, filename + '.' + format)
        if not os.path.isfile(new_filepath):
            raise RuntimeError("Couldn't find a printed PDF under %s" % new_filepath)
        if output_filename:
            output_filename, _tmp_ext = os.path.splitext(output_filename)
            newer_filepath = os.path.join(WEBODT_OPENOFFICE_PDF_PRINTER_OUT, output_filename + '.' + format)
            os.rename(new_filepath, newer_filepath)
            new_filepath = newer_filepath
        fd = Document(new_filepath, mode='r', delete_on_close=delete_on_close)
        return fd
