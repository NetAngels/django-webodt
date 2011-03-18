Backend documentation
=====================

There are three built in converters. To make `django-webodt` usable, you should set up
``WEBODT_CONVERTER`` settings variable to one of the class names:

- ``webodt.converters.abiword.AbiwordODFConverter``
- ``webodt.converters.openoffice.OpenOfficeODFConverter``
- ``webodt.converters.googledocs.GoogleDocsODFConverter``


:mod:`abiword` -- Abiword backend
---------------------------------------------------------------

Backend name::

    WEBODT_CONVERTER = 'webodt.converters.abiword.AbiwordODFConverter'

Abiword backend uses `Abiword <http://http://www.abisource.com/>`_  and
``subprocess`` module to convert files. To make it usable all you have to do is
to install abiword and make sure that it can be lauched with
``WEBODT_ABIWORD_COMMAND``.


:mod:`openoffice` -- OpenOffice backend
----------------------------------------------------------------

Backend name::

    WEBODT_CONVERTER = 'webodt.converters.openoffice.OpenOfficeODFConverter'

This is the most powerful and the heaviest backend. First before the OpenOffice
should be launched as a daemon listening a TCP port for connections (in
headless mode). Headless mode of OpenOffice is a regime of working such that
office detaches itself from console, doesn't open any windows and just starts
haindling incoming requests from other applications.

All you have to do is to choose appropriate network interface (usually you'd
like to bind OpenOffice to loopback) and port (up to your choice, for
example, 2002) to listen to and then type something like this::

    soffice '-accept=socket,host=127.0.0.1,port=2002;urp;StarOffice.NamingService' -headless

In the example above office is listening port 2002 of the loopback interface.
You can use "0" instead of IP-address if you want to make your office to bind
to all available interfaces.

If you work on Linux and you don't want your office process to be daemonized,
use "soffice.bin" instead of "soffice". Ctrl+C will help you to kill running
proccess painlessly. Usually soffice.bin is placed somewhere within
``/usr/lib/openoffice/`` directory.

Once your office is launched, you have to make your application known where it
is located by setting up ``OOFFICE_SERVER`` variable. You need to setup host and
port of the office::

    OOFFICE_SERVER = ('127.0.0.1', 2002)

To make the python code communicate with OpenOffice application, the `PyUNO`
module is required. Name of this module in Ubuntu is `libobasis3.3-pyuno`.

.. warning::
    **Office leaks!** It is a known bug, and if you plan to work more or less
    intensively with this backend, you would probably like to restart it every
    period of time (for example, on a daily basis from cron).

.. autoclass:: webodt.converters.openoffice.OpenOfficeODFConverter
    :members:




:mod:`googledocs` -- Google docs backend
----------------------------------------

Backend name::

    WEBODT_CONVERTER = 'webodt.converters.googledocs.GoogleDocsODFConverter'

This backend uses the google docs API to convert documents. Behind the scene
converter creates new document in docs.google.com with a random name, then
downloads it in a desired format and finally removes the temporary document.

To use the backend it's necessary to have a google account and to set up
``WEBODT_GOOGLEDOCS_EMAIL`` and ``WEBODT_GOOGLEDOCS_PASSWORD`` options.
