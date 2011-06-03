# -*- coding: utf-8 -*-
from django.template import Context
from cStringIO import StringIO
from lxml import etree
import unittest
import webodt
from webodt.preprocessors import unescape_templatetags_preprocessor, xmlfor_preprocessor, _find_common_ancestor



class UnescapeTemplatetagsTest(unittest.TestCase):

    def test_unescape_templatetags_preprocessor(self):
        content = unescape_templatetags_preprocessor(
            u'{% if user == &quot;John Doe&quot; %}&lt;'
            u'{% if balance &gt; 10.00 %}{{ &quot;profit!&quot; }}{% endif %}'
            u'{% endif %}'
        )
        self.assertEqual(content,
            u'{% if user == "John Doe" %}&lt;'
            u'{% if balance > 10.00 %}{{ "profit!" }}{% endif %}'
            u'{% endif %}'
        )

    def test_unescape_in_templates(self):
        template = webodt.ODFTemplate('unescape_templatetags.odt',
            preprocessors=['webodt.preprocessors.unescape_templatetags_preprocessor',]
        )
        context = {'user': 'John Doe'}
        document = template.render(Context(context))
        self.assertTrue(
            'Unescape templatetags works!' in document.get_content_xml()
        )
        document.delete()


class XMLForTest(unittest.TestCase):

    def test_xmlfor_preprocessor(self):
        input_template = '''<table>
            <tr>
                <td>{% xmlfor user in users %}{{ user.username }}</td>
                <td>{{ user.balance }}{% endxmlfor %}</td>
            </tr>
        </table>'''
        expected_output_template = '''<table>
            {% for user in users %}<tr>
                <td>{{ user.username }}</td>
                <td>{{ user.balance }}</td>
            </tr>{% endfor %}
        </table>'''
        output_template = xmlfor_preprocessor(input_template)
        self.assertEqual(output_template, expected_output_template)

    def test_tail_xmlfor_preprocessor(self):
        input_template = '''<table>
            <tr>
                <td><div>hello</div>{% xmlfor user in users %}{{ user.username }}</td>
                <td><div>{{ user.balance }}</div>{% endxmlfor %}</td>
            </tr>
        </table>'''
        expected_output_template = '''<table>
            {% for user in users %}<tr>
                <td><div>hello</div>{{ user.username }}</td>
                <td><div>{{ user.balance }}</div></td>
            </tr>{% endfor %}
        </table>'''
        output_template = xmlfor_preprocessor(input_template)
        self.assertEqual(output_template, expected_output_template)

    def test_find_common_ancestor(self):
        template = '''
        <table>
            <tr>
                <td><p>foo</p></td>
                <td><div><span>bar</span></div></td>
            </tr>
        </table>
        '''
        tree = etree.parse(StringIO(template))
        start = tree.xpath('//table/tr/td/p')[0]
        end = tree.xpath('//table/tr/td/div/span')[0]
        expected_ancestor = tree.xpath('//table/tr')[0]
        ancestor = _find_common_ancestor(start, end)
        self.assertEqual(ancestor, expected_ancestor)
