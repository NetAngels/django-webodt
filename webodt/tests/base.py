# -*- coding: utf-8 -*-
import os
import unittest
import webodt
from cStringIO import StringIO
from django.template import Context
from webodt.converters.abiword import AbiwordODFConverter
from webodt.converters.openoffice import OpenOfficeODFConverter
from webodt.converters.googledocs import GoogleDocsODFConverter


class ODFTemplateTest(unittest.TestCase):

    def test_packed_template(self):
        template = webodt.ODFTemplate('sample.odt')
        content = template.get_content_xml()
        self.assertTrue('{{ username }}' in content)

    def test_unpacked_template(self):
        template = webodt.ODFTemplate('sample')
        content = template.get_content_xml()
        self.assertTrue('{{ username }}' in content)


class ODFDocumentTest(unittest.TestCase):

    def test_file(self):
        for template_name in 'sample sample.odt'.split():
            self._test_file(template_name)

    def _test_file(self, template_name):
        template = webodt.ODFTemplate(template_name)
        context = {
            'username': 'John Doe',
            'balance': 10.01
        }
        document = template.render(Context(context))
        self.assertTrue(os.path.isfile(document.name))
        self.assertTrue('John Doe' in document.get_content_xml())
        document.delete()
        self.assertFalse(os.path.isfile(document.name))

    def test_document_auto_removal(self):
        template = webodt.ODFTemplate('sample.odt')
        context = {
            'username': 'John Doe',
            'balance': 10.01
        }
        document = template.render(Context(context), delete_on_close=True)
        self.assertTrue(os.path.isfile(document.name))
        document.close()
        self.assertFalse(os.path.isfile(document.name))


class AbiwordODFConverterTest(unittest.TestCase):

    def test_converter(self):
        template = webodt.ODFTemplate('sample.odt')
        context = {
            'username': 'John Doe',
            'balance': 10.01
        }
        document = template.render(Context(context))
        converter = AbiwordODFConverter()
        html_document = converter.convert(document, 'html')
        html_data = html_document.read()
        self.assertTrue('John Doe' in html_data)
        document.close()
        html_document.close()
        self.assertFalse(os.path.isfile(document.name))
        self.assertFalse(os.path.isfile(html_document.name))


class GoogleDocsODFConverterTest(unittest.TestCase):

    def test_converter(self):
        template = webodt.ODFTemplate('sample.odt')
        context = {
            'username': 'John Doe',
            'balance': 10.01
        }
        document = template.render(Context(context))
        converter = GoogleDocsODFConverter()
        html_document = converter.convert(document, 'html')
        html_data = html_document.read()
        self.assertTrue('John Doe' in html_data)
        document.close()
        html_document.close()
        self.assertFalse(os.path.isfile(document.name))
        self.assertFalse(os.path.isfile(html_document.name))


class OpenOfficeODFConverterTest(unittest.TestCase):

    def test_converter(self):
        template = webodt.ODFTemplate('sample.odt')
        context = {
            'username': 'John Doe',
            'balance': 10.01
        }
        document = template.render(Context(context))
        converter = OpenOfficeODFConverter()
        html_document = converter.convert(document, 'html')
        html_data = html_document.read()
        self.assertTrue('John Doe' in html_data)
        document.close()
        html_document.close()
        self.assertFalse(os.path.isfile(document.name))
        self.assertFalse(os.path.isfile(html_document.name))
