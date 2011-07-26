Webodt tips and tricks
=======================

What if I open Open Document
--------------------------------

Hopefully, the majority of templates you will need can be created painlessly
with a word processor. Unfortunately, it's sometimes required to create more
complex templates. To make it possible, we will need to open .odt source and to
write a template right there.

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

Template inheritance
--------------------

Although webodt doesn't understand Django template loaders, Django templates
surely do. It is possible to use template inheritance and template inclusion
with no additional efforts from your side. All you have to do is to create the
base template with the contents and blocks and place it into ``TEMPLATES_DIR``
directory. Then it's enough to write in previously mentioned `content.xml`
something like::

    {% extends base_template.xml %}
    {% block content %}
        <text:p text:style-name="Standard">Hello {{ username }}, your
          balance is {{ balance|floatformat:2 }}</text:p>
    {% endblock %}
