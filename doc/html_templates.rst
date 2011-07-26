How to use HTML templaes
==========================

We tried to start using HTML as a base format for templates, but the outcome we
got was fairly disappointing. It's because all known HTML importers are rather
primitive, and it is almost impossible to create document with more or less
sophisticated formatting.

Nonetheless, if you don't intend to use highly complex formatting, you may use
HTML as a basis of templates. There is a special class named
``webodt.HTMLTemplate`` which behaviour is similar to the same of
``webodt.ODFTemplate``. So you can start off with::


    >>> import webodt
    >>> template = webodt.HTMLTemplate('test.html')
