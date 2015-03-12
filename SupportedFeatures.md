## Introduction ##

The definitive [PDF manual](http://www.adobe.com/devnet/acrobat/pdfs/pdf_reference_1-7.pdf) is 1310 pages long.  For the most part, pdfrw tries to be agnostic about the contents of PDF files, and support them as containers, but to do useful work, something a little higher-level is required.

## Missing features ##

Even as a pure PDF container library, pdfrw comes up a bit short.
It does not currently support:

  * Most compression/decompression filters
  * PDF v. 1.5 compressed object streams (now supported in branch [nerijus](http://code.google.com/p/pdfrw/source/browse/#svn%2Fbranches%2Fnerijus))
  * encryption

[pdftk](http://www.accesspdf.com/pdftk/) is a wonderful command-line tool that can convert your PDFs to remove encryption and compression.  However, in most cases, you can do a lot of useful work with PDFs without actually removing compression, because only certain elements inside PDFs are actually compressed.  (This changes somewhat with PDFs designed for version 1.15 and above of the specification.)

## Higher-level capabilities ##

Although pdfrw is mostly a PDF file container library, it supports the following features:

  * PDF pages.  pdfrw knows enough to find the pages in PDF files you read in, and to write a set of pages back out to a new PDF file.
  * Form XObjects.  pdfrw can take any page or rectangle on a page, and convert it to a Form XObject, suitable for use inside another PDF file.
  * reportlab objects.  pdfrw can recursively create a set of reportlab objects from its internal object format.  This allows, for example, Form XObjects to be used inside reportlab.