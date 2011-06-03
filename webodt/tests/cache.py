# -*- coding: utf-8 -*-
import os
from django.utils import unittest
import webodt
from webodt.cache import CacheManager
from webodt.converters import converter
from django.template import Context


class CacheManagerTest(unittest.TestCase):

    def setUp(self):
        self.cache_manager = CacheManager()
        self.converter = converter()

    def test_manager(self):
        template = webodt.ODFTemplate('sample.odt')
        context = {
            'username': 'John Doe',
            'balance': 10.01
        }
        format = 'pdf'
        # check that cache is empty
        odf_document = template.render(Context(context))
        cached_document = self.cache_manager.get(odf_document, format)
        self.assertEqual(cached_document, None)
        # store document to cache
        document = self.converter.convert(odf_document, format)
        self.cache_manager.set(odf_document, format, document)
        # check that cache is not empty
        cached_document = self.cache_manager.get(odf_document, format)
        self.assertEqual(cached_document.read(), document.read())
        # delete data from cache
        self.cache_manager.delete(odf_document, format)
        cached_document = self.cache_manager.get(odf_document, format)
        self.assertEqual(cached_document, None)

    def tearDown(self):
        self.cache_manager.clear()
