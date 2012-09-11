# -*- coding: utf-8 -*-
import os
import zipfile
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
try:
    import tidy
except ImportError:
    XML_FORMAT = False
else:
    XML_FORMAT = True



class Command(BaseCommand):
    args = '[--dir dirname] template.odt'
    help = 'unpack an *.odt template into the directory with given name'

    dir_option = make_option('-d', '--dir', dest='dir',
            help='destination directory name', default=None)
    format_option = make_option('-f', '--format', action='store_true',
            dest='format',
            help='XML pretty print formatting (requires tidy package)', default=False)

    option_list = BaseCommand.option_list + (
        dir_option, format_option
    )

    def handle(self, *args, **options):
        self.args = args
        self.options = options
        self.filename = self._get_odt_file()
        self.dirname = self._get_output_directory()
        self._make_output_directory()
        fd = zipfile.ZipFile(self.filename, mode='r')
        fd.extractall(path=self.dirname)
        if options['format'] and XML_FORMAT:
            self._xml_format()


    def _get_odt_file(self):
        if len(self.args) < 1:
            raise CommandError('odt file is not defined')
        if len(self.args) > 1:
            raise CommandError('Sorry, I can handle only one .odt file at a time')
        full_path = os.path.join(settings.WEBODT_FILE_DIR, self.args[0])
        if not os.path.isfile(full_path):
            raise CommandError('File %s not found' % full_path)
        return full_path


    def _get_output_directory(self):
        if self.options['dir'] != None:
            return self.options['dir']
        basename = os.path.basename(self.filename)
        chunks = basename.split('.')
        if len(chunks) > 1:
            return '.'.join(chunks[:-1])
        else:
            return basename


    def _make_output_directory(self):
        if not os.path.isdir(self.dirname):
            os.makedirs(self.dirname)


    def _xml_format(self):
        for dirname, _, files in os.walk(self.dirname):
            for filename in files:
                full_name = os.path.join(dirname, filename)
                if full_name.endswith('.xml'):
                    i = open(full_name, 'r')
                    obj = tidy.parseString(i.read(), **self._tidy_options)
                    i.close()
                    o = open(full_name, 'w')
                    obj.write(o)


    _tidy_options = {
        'indent': True,
        'indent-spaces': 4,
        'wrap': 0,
        'char-encoding': 'utf8',
        'input-xml': True,
        'output-xml': True,
        # 'write-back': True,
    }
