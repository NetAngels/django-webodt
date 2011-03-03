**django-webodt** is a django module which aims to create documents in various
formats from Open Document templates (odt). Django-webodt supports virtually
all formats supported by chosen backend tool. We have positive experience of
creating PDF, HTML, RDF and MS Word (.doc) documents.

Document conversion is performed with help of external tools, each of which is
served by its own backend. Currently there are three built-in backends:

- **ooffice**: performs format conversion using big and fat OpenOffice.
  Especially suitable for documents with complicated formatting, where all
  other backends can fail. OpenOffice should be launched as daemon before.
- **abiword**: relatively lightweight converter which uses abiword as
  converting engine.  Best choice for those who have restricted amount of
  resources and/or don't want to worry about daemon launching.
- **googledocs**: uses free service from Google, the only possible variant for
  shared-hosting users or users with limited amount of resources who don't care
  much about their privacy.
