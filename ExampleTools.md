## Introduction ##

The examples directory has a few scripts which use the library.

## Simplest scripts -- subset, 4up, and poster ##

A tiny example which will extract a subset of pages from a PDF file:
> http://code.google.com/p/pdfrw/source/browse/trunk/examples/subset.py

> Same example, using reportlab for PDF output:
> > http://code.google.com/p/pdfrw/source/browse/trunk/examples/rl1/subset.py

An example which converts a PDF into a 4-up PDF:

> http://code.google.com/p/pdfrw/source/browse/trunk/examples/4up.py

> Same example, using reportlab for PDF output:
> > http://code.google.com/p/pdfrw/source/browse/trunk/examples/rl1/4up.py

An example which upsizes a letter-sized PDF to a 48 x 36" poster:

> http://code.google.com/p/pdfrw/source/browse/trunk/examples/poster.py

A tiny example which will rotate all or selected pages in a PDF file:
> http://code.google.com/p/pdfrw/source/browse/trunk/examples/rotate.py

## Slightly more complicated -- booklet ##

A printer with a fancy printer and/or a full-up copy of Acrobat can easily turn your small PDF into a little booklet (for example, print 4 letter-sized pages on a single 11" x 17").

But that assumes several things, including that the personnel know how to operate the hardware and software.  booklet.py lets you turn your PDF into a preformatted booklet, to give them fewer chances to mess it up:

> http://code.google.com/p/pdfrw/source/browse/trunk/examples/booklet.py

> Same example, using reportlab for PDF output.
> > http://code.google.com/p/pdfrw/source/browse/trunk/examples/rl1/booklet.py

## Watermarking PDFs ##

The watermark demo takes two PDFs, and creates a merged PDF using one of
the source PDFs to place a watermark on top of every page of the other source PDF:


> http://code.google.com/p/pdfrw/source/browse/trunk/examples/watermark.py

A different approach uses a preexisting PDF as a background watermark for
pages created programmatically with reportlab.  This demo was contributed by
user asannes:

> http://code.google.com/p/pdfrw/source/browse/trunk/examples/rl1/platypus_pdf_template.py

## Adding or modifying metadata ##

The metadata example will accept multiple input files on the command line, concatenate them and output them to output.pdf, after adding some nonsensical metadata to the output PDF file:

> http://code.google.com/p/pdfrw/source/browse/trunk/examples/metadata.py

The alter.py example alters a single metadata item in a PDF, and writes the result to a new PDF:

> http://code.google.com/p/pdfrw/source/browse/trunk/examples/alter.py

## Rotating and doubling -- print\_two ##

If you ever want to print something that is like a small booklet, but needs to be spiral bound, you either have to do some fancy rearranging, or just waste half your paper.

The print\_two example program will, for example, make two side-by-side copies each page of of your PDF on a each output sheet.

But, every other page is flipped, so that you can print double-sided and the pages will line up properly and be pre-collated:
> http://code.google.com/p/pdfrw/source/browse/trunk/examples/print_two.py

## Graphics stream parsing proof of concept ##

This script shows a simple example of reading in a PDF, and using the decodegraphics.py module to try to write the same information out to a new PDF through a reportlab canvas.  (If you know about reportlab, you know that if you can faithfully render a PDF to a reportlab canvas, you can do pretty much anything else with that PDF you want.)  This kind of low level manipulation should be done only if you really need to.  decodegraphics is really more than a proof of concept than anything else.  For most cases, just use the Form XObject capability, as shown in the examples/rl1/booklet.py demo:

> http://code.google.com/p/pdfrw/source/browse/trunk/examples/rl2/copy.py