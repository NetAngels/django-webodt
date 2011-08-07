# -*- coding: utf8 -*-
from django.test.client import Client
from django.utils import unittest
from webodt.shortcuts import render_to, render_to_response
from django.core.urlresolvers import reverse

class RenderToTest(unittest.TestCase):

    def test_render_to(self):
        context = {
            'username': 'John Doe',
            'balance': 10.01
        }
        html_fd = render_to('html', 'sample.odt', context)
        html_data = html_fd.read()
        html_fd.close()
        self.assertTrue('John Doe' in html_data)

    def test_html_render_to(self):
        context = {
            'username': 'John Doe',
            'balance': 10.01
        }
        html_fd = render_to('html', 'sample.html', context)
        html_data = html_fd.read()
        html_fd.close()
        self.assertTrue('John Doe' in html_data)

    def test_render_to_response(self):
        context = {
            'username': 'John Doe',
            'balance': 10.01
        }
        response = render_to_response('sample.odt', dictionary=context,
                                      format='html')
        self.assertTrue('John Doe' in response.content)

    def test_render_to_response_in_view(self):
        client = Client()
        path = reverse('webodt-test-pdf')
        response = client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content))
