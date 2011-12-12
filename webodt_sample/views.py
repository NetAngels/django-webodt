#coding:utf-8
from django.template.context import RequestContext
from webodt.shortcuts import render_to_response


def test_pdf(request):
    context = {'username': 'John Doe', 'balance': 10.01}
    return render_to_response('sample.odt',
        dictionary=context, format='pdf', filename='test.pdf',
        context_instance=RequestContext(request)
    )


def test_pdf_from_html(request):
    context = {'username': 'John Doe', 'balance': 10.01}
    return render_to_response('sample.html',
        dictionary=context, format='pdf', filename='test1.pdf',
        context_instance=RequestContext(request), cache=None,
    )


def test_iterator(request):
    iterator = request.GET.get('iterator') == 'true'
    context = {'username': 'John Doe', 'balance': 10.01}
    return render_to_response('sample.odt',
        dictionary=context, format='html', filename='test.html',
        iterator=iterator,
    )
