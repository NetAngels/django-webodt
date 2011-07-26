Settings options
================

There is a number of options used by the `django-webodt`. Most of options are
required only for the particular backend.

+--------------------------------------+-----------------------------------------------------------------+-----------------------------------------------------+
| Variable name                        | Default value                                                   | Description                                         |
+======================================+=================================================================+=====================================================+
|``WEBODT_TEMPLATE_PATH``              | ``''``                                                          | Root directory for webodt templates `(required)`    |
+--------------------------------------+-----------------------------------------------------------------+-----------------------------------------------------+
|``WEBODT_DEFAULT_FORMAT``             | ``'doc'``                                                       | Default format to convert to. Not very useful       |
|                                      |                                                                 | since it's more convenient to set the corresponding |
|                                      |                                                                 | variable each time the conversion is performed      |
|                                      |                                                                 |                                                     |
+--------------------------------------+-----------------------------------------------------------------+-----------------------------------------------------+
|``WEBODT_ABIWORD_COMMAND``            | ``['/usr/bin/abiword', '--plugin', 'AbiCommand']``              | Command for running abiword processor to convert    |
|                                      |                                                                 | documents. Should be taken care of only if the      |
|                                      |                                                                 | abiword converter is used.                          |
|                                      |                                                                 |                                                     |
+--------------------------------------+-----------------------------------------------------------------+-----------------------------------------------------+
|``WEBODT_GOOGLEDOCS_EMAIL``           | ``None``                                                        | Email (in the form `username@gmail.com`) of the     |
|                                      |                                                                 | Google account when the googledocs backend is used. |
|                                      |                                                                 |                                                     |
+--------------------------------------+-----------------------------------------------------------------+-----------------------------------------------------+
|``WEBODT_GOOGLEDOCS_PASSWORD``        | ``None``                                                        | Password for the Google account when the            |
|                                      |                                                                 | googledocs backend is used                          |
|                                      |                                                                 |                                                     |
+--------------------------------------+-----------------------------------------------------------------+-----------------------------------------------------+
|``WEBODT_OPENOFFICE_SERVER``          | ``('localhost', 2002)``                                         | Address (host and port of the OpenOffice server     |
|                                      |                                                                 | when the openoffice backend is used. See backend    |
|                                      |                                                                 | related documentation to get more information.      |
|                                      |                                                                 |                                                     |
+--------------------------------------+-----------------------------------------------------------------+-----------------------------------------------------+
|``WEBODT_CONVERTER``                  | ``'webodt.converters.abiword.AbiwordODFConverter'``             | Default ODF to other formats converter.  You don't  |
|                                      |                                                                 | need to take care of it you plan to generate ODF    |
|                                      |                                                                 | documents only.                                     |
|                                      |                                                                 |                                                     |
+--------------------------------------+-----------------------------------------------------------------+-----------------------------------------------------+
|``WEBODT_CACHE_DIR``                  | ``'/tmp/webodt_cache'``                                         | Directory to store cache files by the cache manager |
|                                      |                                                                 |                                                     |
|                                      |                                                                 |                                                     |
+--------------------------------------+-----------------------------------------------------------------+-----------------------------------------------------+
|``WEBODT_ODF_TEMPLATE_PREPROCESSORS`` |                                                                 | List of webodt template preprocessors               |
|                                      | - webodt.preprocessors.xmlfor_preprocessor,                     |                                                     |
|                                      | - webodt.preprocessors.unescape_templatetags_preprocessor       |                                                     |
|                                      |                                                                 |                                                     |
+--------------------------------------+-----------------------------------------------------------------+-----------------------------------------------------+
