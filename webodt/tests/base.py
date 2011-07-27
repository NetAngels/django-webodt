# -*- coding: utf-8 -*-
import os
from django.utils import unittest
import webodt
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

    def test_html_template(self):
        template = webodt.HTMLTemplate('sample.html')
        content = template.get_content()
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
        self.assertEqual(os.stat(document.name).st_mode & 0777, 0600)
        self.assertEqual(document.format, 'odt')
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


class HTMLDocumentTest(unittest.TestCase):

    def test_file(self):
        template = webodt.HTMLTemplate('sample.html')
        context = {
            'username': 'John Doe',
            'balance': 10.01
        }
        document = template.render(Context(context), delete_on_close=True)
        self.assertTrue(os.path.isfile(document.name))
        self.assertEqual(os.stat(document.name).st_mode & 0777, 0600)
        self.assertEqual(document.format, 'html')
        self.assertTrue('John Doe' in document.get_content())
        document.delete()
        self.assertFalse(os.path.isfile(document.name))

    def test_utf8(self):
        template = webodt.HTMLTemplate('sample.html')
        context = {
            'username': u'Тест',
            'balance': 10.01
        }
        document = template.render(Context(context), delete_on_close=True)
        self.assertTrue(os.path.isfile(document.name))
        self.assertTrue('Тест' in document.get_content()) # we compare bytes, not unicode symbols
        document.delete()


class _ConverterTest(object):
    context = {
        'username': 'John Doe',
        'balance': 10.01
    }
    Converter = None

    def test_converter(self):
        template = webodt.ODFTemplate('sample.odt')
        document = template.render(Context(self.context))
        converter = self.Converter()
        html_document = converter.convert(document, 'html')
        html_data = html_document.read()
        self.assertTrue('John Doe' in html_data)
        document.close()
        html_document.close()
        self.assertFalse(os.path.isfile(document.name))
        self.assertFalse(os.path.isfile(html_document.name))

    def test_html_converter(self):
        template = webodt.HTMLTemplate('sample.html')
        document = template.render(Context(self.context), delete_on_close=False)
        converter = self.Converter()
        odt_document = converter.convert(document, 'odt', delete_on_close=False)
        odt_document2 = webodt.ODFDocument(odt_document.name, delete_on_close=False)
        self.assertTrue('John' in odt_document2.get_content_xml())
        document.close()
        document.delete()
        odt_document.close()
        odt_document.delete()

class AbiwordODFConverterTest(_ConverterTest, unittest.TestCase):
    Converter = AbiwordODFConverter


class GoogleDocsODFConverterTest(_ConverterTest, unittest.TestCase):
    Converter = GoogleDocsODFConverter


class OpenOfficeODFConverterTest(_ConverterTest, unittest.TestCase):
    Converter = OpenOfficeODFConverter
