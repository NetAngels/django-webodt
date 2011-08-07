#coding:utf-8
from django.template.context import RequestContext
from webodt.shortcuts import render_to_response


def test_pdf(request):
    context = {'username': 'John Doe', 'balance': 10.01}
    return render_to_response('sample.odt',
        dictionary=context, format='pdf', filename='test.pdf',
        context_instance=RequestContext(request)
    )