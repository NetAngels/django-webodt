# -*- coding: utf-8 -*-
import os
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError



class Command(BaseCommand):
    help = ('simple wrapper to launch OpenOffice/LibreOffice in a headless mode '
            'without detaching from the console')

    option_list = BaseCommand.option_list + (
        make_option('-H', '--host',
                    help='hostname which office application should bind to',
                    default='127.0.0.1'),
        make_option('-p', '--port',
                    type='int',
                    help='port number which office application should bind to',
                    default=2002),
        make_option('-x', '--executable',
                    help='path to the OpenOffice/LibreOffice executable'),
    )

    office_location_variants = [
        '/usr/lib/libreoffice/program/soffice.bin',
        '/usr/lib/openoffice/program/soffice.bin',
    ]


    def handle(self, *args, **options):
        path = self.get_office_path(options['executable'])
        accept_arg = ('--accept=socket,host={host},port={port};urp;'
                      'StarOffice.NamingService').format(**options)
        self.stdout.write('Launching OpenOffice.\n')
        os.execv(path, [path, accept_arg, '--headless'])

    def get_office_path(self, suggested_path):
        if suggested_path:
            if not os.path.isfile(suggested_path):
                raise CommandError('{0} not found'.format(suggested_path))
            return suggested_path
        for variant in self.office_location_variants:
            if os.path.isfile(variant):
                return variant
        raise CommandError('I cannot find soffice in any pre-defined location. '
                           'Please specify the location with the --executable option. '
                           'Feel free also to ask the author to include this '
                           'path to the list of well-known locations. The issue '
                           'tracker is available at '
                           'https://github.com/NetAngels/django-webodt/issues')
