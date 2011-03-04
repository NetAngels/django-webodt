# -*- coding: utf-8 -*-
import uno, unohelper
from com.sun.star.io import IOException, XOutputStream, XSeekable, XInputStream
from com.sun.star.beans import PropertyValue
from webodt import Document
from webodt.converters import ODFConverter
from webodt.conf import WEBODT_OPENOFFICE_SERVER

OOO_CONNECTION = 'socket,host=%s,port=%s;urp;StarOffice.ComponentContext' % WEBODT_OPENOFFICE_SERVER


class OpenOfficeODFConverter(ODFConverter):


    def convert(self, document, format=None, output_filename=None, delete_on_close=True):
        output_filename, format = self._guess_format_and_filename(output_filename, format)
        ### Do the OpenOffice component dance
        context = uno.getComponentContext()
        resolver = context.ServiceManager.createInstanceWithContext('com.sun.star.bridge.UnoUrlResolver', context)
        unocontext = resolver.resolve('uno:%s' % OOO_CONNECTION)
        ### And some more OpenOffice magic
        unosvcmgr = unocontext.ServiceManager
        desktop = unosvcmgr.createInstanceWithContext('com.sun.star.frame.Desktop', unocontext)
        config = unosvcmgr.createInstanceWithContext('com.sun.star.configuration.ConfigurationProvider', unocontext)
        ### Load inputfile
        instream = InputStream(uno.ByteSequence(document.read()))
        inputprops = [
            PropertyValue('InputStream', 0, instream, 0),
        ]
        if document.format == 'html':
            inputprops.append(PropertyValue('FilterName', 0, 'HTML (StarWriter)', 0))
        doc = desktop.loadComponentFromURL('private:stream','_blank',0, tuple(inputprops))
        ### Update document links
        # skip ...
        ### Update document indexes
        # skip ...
        ### Write outputfile
        fd = open(output_filename, 'w')
        filter_name = formats[format]
        outputprops = [
            PropertyValue('FilterData', 0, uno.Any('[]com.sun.star.beans.PropertyValue', tuple(),), 0),
            PropertyValue('FilterName', 0, filter_name, 0),
            PropertyValue('OutputStream', 0, OutputStream(fd), 0),
            PropertyValue('Overwrite', 0, True, 0),
        ]
        if filter_name == 'Text (encoded)':
            outputprops.append(PropertyValue('FilterFlags', 0, 'UTF8, LF', 0))
        doc.storeToURL('private:stream', tuple(outputprops))
        doc.dispose()
        doc.close(True)
        fd.close()
        fd = Document(output_filename, mode='r', delete_on_close=delete_on_close)
        return fd



formats = {
    'bib': 'BibTeX_Writer',
    'doc': 'MS Word 97',
    'odt': 'writer8',
    'pdf': 'writer_pdf_Export',
    'rtf': 'Rich Text Format',
    'txt': 'Text (encoded)',
    'html': 'XHTML Writer File',
}

class OutputStream(unohelper.Base, XOutputStream):
    def __init__(self, descriptor=None):
        self.descriptor = descriptor
        self.closed = 0

    def closeOutput(self):
        self.closed = 1
        if not self.descriptor.isatty:
            self.descriptor.close()

    def writeBytes(self, seq):
        self.descriptor.write(seq.value)

    def flush(self):
        pass


class InputStream(XSeekable, XInputStream, unohelper.Base):
      def __init__(self, seq):
          self.s = seq
          self.nIndex = 0
          self.closed = 0

      def closeInput(self):
          self.closed = 1
          self.s = None

      def skipBytes(self, nByteCount):
          if(nByteCount + self.nIndex > len(self.s)):
              nByteCount = len(self.s) - self.nIndex
          self.nIndex += nByteCount

      def readBytes(self, retSeq, nByteCount):
          nRet = 0
          if(self.nIndex + nByteCount > len(self.s)):
              nRet = len(self.s) - self.nIndex
          else:
              nRet = nByteCount
          retSeq = uno.ByteSequence(self.s.value[self.nIndex : self.nIndex + nRet ])
          self.nIndex = self.nIndex + nRet
          return nRet, retSeq

      def readSomeBytes(self, retSeq , nByteCount):
          #as we never block !
          return readBytes(retSeq, nByteCount)

      def available(self):
          return len(self.s) - self.nIndex

      def getPosition(self):
          return self.nIndex

      def getLength(self):
          return len(self.s)

      def seek(self, pos):
          self.nIndex = pos

