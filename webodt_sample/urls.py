from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^test/pdf/', 'views.test_pdf', name='webodt-test-pdf'),
    url(r'^test/iterator/', 'views.test_iterator', name='webodt-test-iterator'),
)
