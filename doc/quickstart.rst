Quickstart guide
================

To create odt template, it's usially enough to unzip odt file, replace its
content.xml and then re-pack the direcory back or store it as is. Files
"patched" such a way as well as directories containing unzipped and patched odt
content, are called odt templates.

For the simplest .odt templates you don't even have to perform any kind of
zip-manipulation. It's enough to write a document with Django markup right in
the word processor.

There are two main purposes of the webodt

1. Generate fully functional .odt documents on a basis of odt templates,
   prepared manually before.
2. With help of external backend do convert ODF or HTML documents to .pdf,
   .doc, .rtf or any other format, supported by the backend.


Quickstart
---------

Let's get an example of basic django-webodt usage in your Django project.
First, download and install django-webodt::

    pip install django-webodt

Then add webodt to the set of your application. Edit `settings.py`::

    INSTALLED_APPS = (
        ...
        'webodt',
    )

Next you have to decide which backend you want to use. Assuming that you are
under Linux, install Abiword_. Perhaps everything will work under Windows too,
but no one has this checked yet. Mark abiword as your backend of choice in
`settings.py`::

    WEBODT_CONVERTER = 'webodt.converters.abiword.AbiwordODFConverter'

Decide where you want to store your .odt templates. Webodt does not know yet
how to use standard Django template loaders, so please define a directory to
store your odt templates (sure enough, it's possible to use the same directory
where all other templates are stored)::

    WEBODT_TEMPLATE_PATH = '.../webodt/templates/'

It's about time to create your first .odt template. Just open word editor
(abiword, for example) and create something like on a screenshot below. Save
the template in ``WEBODT_TEMPLATE_PATH`` under the name `test.odt`.

.. image:: _static/abiword.png

Now webodt is ready to work.  Steps below demonstrate how to use webodt to
create a pdf from this template.

Let's first create a fully fledged .odt document from the template. We replace
variables `user` and `balance` with appropriate values::

    $ ./manage.py shell

    >>> from django.template import Context
    >>> import webodt
    >>> template = webodt.ODFTemplate('test.odt')
    >>> context = dict(user='John Doe', balance=10.05)
    >>> document = template.render(Context(context))

It have to be mentioned, that the document object we have created is just an
open file in a nutshell::

    >>> document
    <open file '/tmp/tmpL0AKCV.odt', mode 'rb' at 0xa7c39ec>

This is a real file. The file is available to any other application. Open
`/tmp/tmpL0AKCV.odt` to make sure it's true. But there is something special
about the file too::

    >>> document.__class__
    <class 'webodt.ODFDocument'>
    >>> import os
    >>> os.path.isfile(document.name)
    True
    >>> document.close()
    >>> os.path.isfile(document.name)
    False

Being closed, document is automatically removed from the disk. It is important
that you close all your documents, otherwise you risk to produce a lot of
garbage in `/tmp` directory. You can prevent auto deletion by passing
``delete_on_close=False`` to ``render`` method of the template.

Let's make yet another document to continue our research and convert it to
pdf::

    >>> document = template.render(Context(context))

Create converter and make it do the job::

    >>> from webodt.converters import converter
    >>> conv = converter()
    >>> pdf = conv.convert(document, format='pdf')
    >>> pdf
    <open file '/tmp/tmpYuAhhN.pdf', mode 'r' at 0xa7c3dfc>

Resulting file looks very similar to that one we have created with ``render``
method previously. It will be removed when closed, and, similarly this
behaviour can be disabled with an option, passed as function variable.
Additionally, resulting document can be created with another, more meaningful
name (it's defined with another option named ``output_filename``).

Having open the document, you get

.. image:: _static/evince.png

To get to know more, feel free to refer full documentation.

.. _Abiword: http://www.abisource.com/



What if I open Open Document
--------------------------------

We have mentioned above a very basic example of template. Templates like this
are painlessly created with a word processor. Sure enough, it's often needed to
create more complex templates, especially when dealing with tables. To make it
possible, we will need to open .odt source and to write a template right there.

It is well known that Open Document (odt file) is nothing but a zipped
directory with a bunch of XML-files and images. It is less known that the
format of the package is rather straighforward and can be easily grasped
without extensive manual learning.

If you try to unzip odt document, you will find a set of files like
`content.xml`, `manifest.rdf`, `meta.xml` and so on inside. Usually,
`content.xml` is the biggest file with all the content. Other files can be
considered as auxiliaries.

Although ordinary XML, content.xml is not very convenient to observe, because
usually word processors don't insert line wraps between tags. One of the
easiest way to make it eye-safe is to use "tidy" utility::

    tidy -modify -xml -utf8 -indent content.xml

After that and throwing out all XML redundance, you see something like this::

    <?xml version="1.0" encoding="utf-8"?>
    <office:document-content  ....>
      <office:body>
        <office:text>
          ...
          <text:p text:style-name="Standard">Hello {{ username }}, your
          balance is {{ balance|floatformat:2 }}</text:p>
        </office:text>
      </office:body>
    </office:document-content>

Finally, this is the template, ready to modify and use. You can apply all
Django filters and tags inside, create loops, conditionals, etc. Behind the
scene webodt unpacks .odt file, parse `content.xml` with Django template
processor, zip everything back and then, if needed, passes resulting document
through the backend to get the document in other format.


What about HTML templates?
--------------------------

We tried to start using HTML as a base format for templates, but the outcome we
got was fairly disappointing. It's because all known HTML importers are rather
privitive, and it is almost impossible to create document with more or less
sophisticated formatting.

Nonetheless, if you don't intend to use highly complex formatting, you may use
HTML as a basis of templates. There is a special class named
``webodt.HTMLTemplate`` which behaviour is similar to the same of
``webodt.ODFTemplate``. So you can start off with::


    >>> import webodt
    >>> template = webodt.HTMLTemplate('test.html')


Template inheritance
--------------------

Although webodt doesn't understand Django template loaders, Django templates
surely do. It makes it possible to use template inheritance and template
inclusion with no additional efforts from your side. All you have to do is to
create the base template with the contents and blocks and place it into
``TEMPLATES_DIR`` directory. Then it's enough to write in previously mentioned
`content.xml` something like::

    {% extends base_template.xml %}
    {% block content %}
        <text:p text:style-name="Standard">Hello {{ username }}, your
          balance is {{ balance|floatformat:2 }}</text:p>
    {% endblock %}
