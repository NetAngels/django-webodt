# -*- coding: utf-8 -*-
from django.template import Context
from webodt.preprocessors import unescape_templatetags
import unittest
import webodt


class PreprocessorsTest(unittest.TestCase):

    def test_unquote_templatetags(self):
        content = unescape_templatetags(
            u'{% if user == &quot;John Doe&quot; %}&lt;'
            u'{% if balance &gt; 10.00 %}{{ &quot;profit!&quot; }}{% endif %}'
            u'{% endif %}'
        )
        self.assertEqual(content,
            u'{% if user == "John Doe" %}&lt;'
            u'{% if balance > 10.00 %}{{ "profit!" }}{% endif %}'
            u'{% endif %}'
        )

    def test_unquote_in_templates(self):
        template = webodt.ODFTemplate('unescape_templatetags.odt',
            preprocessors=['webodt.preprocessors.unescape_templatetags',]
        )
        context = {'user': 'John Doe'}
        document = template.render(Context(context))
        self.assertTrue(
            'Unescape templatetags works!' in document.get_content_xml()
        )
        document.delete()
