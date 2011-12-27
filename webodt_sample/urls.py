from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^test/pdf/$', 'views.test_pdf', name='webodt-test-pdf'),
    url(r'^test/iterator/$', 'views.test_iterator', name='webodt-test-iterator'),
    url(r'^test/pdf_from_html/$', 'views.test_pdf_from_html', name='webodt-test-pdf-from-html'),
)
