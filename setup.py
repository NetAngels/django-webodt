#!/usr/bin/env python
# -*- coding: utf8 -*-
from distutils.core import setup

import os, sys
reload(sys).setdefaultencoding("UTF-8")

def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except:
        return ''

setup(
    name='django-webodt',
    version='0.2',
    author='NetAngels',
    author_email='info@netangels.ru',
    packages=['webodt', 'webodt.converters',],
    url='http://github.com/netangels/django-webodt',
    license = 'BSD License',
    description = u'ODF template handler and odt to html, pdf, doc, etc converter',
    long_description = read('README.rst'),
    install_requires = [
        'Django',
        'lxml',
    ],
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
