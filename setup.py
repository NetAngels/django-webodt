#!/usr/bin/env python
# -*- coding: utf8 -*-
from distutils.core import setup

import sys
reload(sys).setdefaultencoding("UTF-8")

setup(
    name='django-webodt',
    version='0.2',
    author='NetAngels',
    author_email='info@netangels.ru',
    packages=['webodt', 'webodt.converters',],
    url='http://github.com/netangels/django-webodt',
    license = 'BSD License',
    description = u'ODF template handler and odt to html, pdf, doc, etc converter',
    long_description = open('README.rst').read().decode('utf8'),
    classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ),
)
