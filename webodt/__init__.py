# -*- coding: utf-8 -*-
"""
Whereas Django Templates accept string as template source, there is
inconvenient way of working with ODF template, because ODF work with a
relatively complex structure and it's easier to pass just template_name.

ODFTemplate accepts both packed (regular) or unpacked .odt documents as
templates. Unpacked ODFTemplate is nothing more than just unzipped .odt file.
"""
import os
import zipfile
import tempfile
import shutil
import time
from django.template import Template
from django.utils.encoding import smart_str
from webodt.conf import WEBODT_TEMPLATE_PATH


class HTMLTemplate(object):
    """ HTML template class """
    format = 'html'
    content_type = 'text/html'

    def __init__(self, template_name):
        """ Create object by the template name. The template name is relative
        to ``WEBODT_TEMPLATE_PATH`` directory. """
        self.template_name = template_name
        self.template_path = os.path.join(WEBODT_TEMPLATE_PATH, template_name)
        if not os.path.isfile(self.template_path):
            raise ValueError('Template %s not found in directory %s' % (template_name, WEBODT_TEMPLATE_PATH))

    def get_content(self):
        fd = open(self.template_path, 'r')
        content = fd.read()
        fd.close()
        return content

    def render(self, context, delete_on_close=True):
        """ Return rendered HTML (webodt.HTMLDocument instance) """
        # get rendered content
        template = Template(self.get_content())
        content = template.render(context)
        # create and return .html file
        _, tmpfile = tempfile.mkstemp(suffix='.html')
        fd = open(tmpfile, 'w')
        fd.write(smart_str(content))
        fd.close()
        # return HTML document
        return HTMLDocument(tmpfile, delete_on_close=delete_on_close)

class ODFTemplate(object):
    """
    ODF template class
    """

    format = 'odt'
    content_type = 'application/vnd.oasis.opendocument.text'
    _fake_timestamp = time.mktime((2010,1,1,0,0,0,0,0,0))

    def __init__(self, template_name):
        """ Create object by the template name. The template name is relative
        to ``WEBODT_TEMPLATE_PATH`` directory.

        template_name: name of the template to load and handle
        """
        self.template_name = template_name
        self.template_path = os.path.join(WEBODT_TEMPLATE_PATH, template_name)
        if os.path.isfile(self.template_path):
            self.packed = True
            self.handler = _PackedODFHandler(self.template_path)
        elif os.path.isdir(self.template_path):
            self.packed = False
            self.handler = _UnpackedODFHandler(self.template_path)
        else:
            raise ValueError('Template %s not found in directory %s' % (template_name, WEBODT_TEMPLATE_PATH))

    def get_content_xml(self):
        """ Return the content.xml file contents """
        return self.handler.get_content_xml()


    def render(self, context, delete_on_close=True):
        """ Return rendered ODF (webodt.ODFDocument instance)"""
        # create temp output directory
        tmpdir = tempfile.mkdtemp()
        self.handler.unpack(tmpdir)
        # store updated content.xml
        template = Template(self.get_content_xml())
        content_xml = template.render(context)
        content_filename = os.path.join(tmpdir, 'content.xml')
        content_fd = open(content_filename, 'w')
        content_fd.write(smart_str(content_xml))
        content_fd.close()
        # create .odt file
        _, tmpfile = tempfile.mkstemp(suffix='.odt')
        tmpzipfile = zipfile.ZipFile(tmpfile, 'w')
        for root, _, files in os.walk(tmpdir):
            for fn in files:
                path = os.path.join(root, fn)
                os.utime(path, (self._fake_timestamp, self._fake_timestamp))
                fn = os.path.relpath(path, tmpdir)
                tmpzipfile.write(path, fn)
        tmpzipfile.close()
        # remove directory tree
        shutil.rmtree(tmpdir)
        # return ODF document
        return ODFDocument(tmpfile, delete_on_close=delete_on_close)



class _PackedODFHandler(object):

    def __init__(self, filename):
        self.filename = filename

    def get_content_xml(self):
        fd = zipfile.ZipFile(self.filename)
        data = fd.read('content.xml')
        fd.close()
        return data

    def unpack(self, dstdir):
        fd = zipfile.ZipFile(self.filename)
        fd.extractall(path=dstdir)
        fd.close()


class _UnpackedODFHandler(object):

    def __init__(self, dirname):
        self.dirname = dirname

    def get_content_xml(self):
        fd = open(os.path.join(self.dirname, 'content.xml'), 'r')
        data = fd.read()
        fd.close()
        return data

    def unpack(self, dstdir):
        os.rmdir(dstdir)
        shutil.copytree(self.dirname, dstdir)


class Document(file):

    def __init__(self, filename, mode='rb', buffering=1, delete_on_close=True):
        file.__init__(self, filename, mode, buffering)
        self.delete_on_close = delete_on_close

    def delete(self):
        os.unlink(self.name)

    def close(self):
        file.close(self)
        if self.delete_on_close:
            self.delete()


class HTMLDocument(Document):
    format = 'html'
    content_type = 'text/html'

    def get_content(self):
        fd = open(self.name, 'r')
        content = fd.read()
        fd.close()
        return content


class ODFDocument(Document):
    format = 'odt'
    content_type = 'application/vnd.oasis.opendocument.text'

    def get_content_xml(self):
        fd = zipfile.ZipFile(self.name)
        data = fd.read('content.xml')
        fd.close()
        return data
