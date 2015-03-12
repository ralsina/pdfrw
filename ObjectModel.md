## Introduction ##

In general, PDF files conceptually map quite well to Python.  The major objects to think about are:

  * **strings**.  Most things are strings.  These also often decompose naturally into
  * **lists of tokens**.  Tokens can be combined to create higher-level objects like
  * **arrays** and
  * **dictionaries** and
  * **Contents streams** (which can be more streams of tokens)

## Difficulties ##

The apparent primary difficulty in mapping PDF files to Python is the PDF file concept of
"indirect objects."  But an indirect object is really just a way to get around
the chicken and egg problem of circular object references when mapping arbitrary
data structures to files.  To flatten out a circular reference, an indirect object
is _referred to_ instead of being _directly included_ in another object.  PDF files
have a global mechanism for locating indirect objects, and they all have two reference
numbers (a reference number and a "generation" number, in case you wanted to append
to the PDF file rather than just rewriting the whole thing).

pdfrw automatically handles indirect references on reading in a PDF file.  When pdfrw
encounters an indirect PDF file object, the corresponding Python object it creates
will have an 'indirect' attribute with a value of True.  When writing a PDF file, if you have created arbitrary data, you just need to make sure that circular references are broken up by putting an attribute named 'indirect' which evaluates to True on at least one object in every cycle.

Another PDF file object that doesn't quite map to regular Python is a "stream".  Streams are dictionaries which each have an associated unformatted data block.  pdfrw handles streams by placing a special attribute on a subclassed dictionary.

## Usage Model ##

The usage model for pdfrw treats most objects as strings (it takes their string representation when writing them to a file).  The two main exceptions are the PdfArray object and the PdfDict object.

PdfArray is just a subclass of list with an 'indirect' attribute, but on writing a PDF file, a regular list would be converted to its str() representation (probably not what you want) while a PdfArray will be turned into a PDF file array.

PdfDict is slightly more functional.  For starters, it is a subclass of dict, also with an 'indirect' attribute (and the subclassed IndirectPdfDict has this automatically set True).

But PdfDict also has an optional associated stream.  The stream object defaults to None, but if you assign a stream to the dict, it will automatically set the PDF /Length attribute for the dictionary.

Finally, since PdfDict instances are indexed by PdfName objects (which always start with a /) and since most (all?) standard Adobe PdfName objects use names formatted like "/CamelCase", it makes sense to allow access to dictionary elements via object attribute accesses as well as object index accesses.  So usage of PdfDict objects is normally via attribute access, although non-standard names (though still with a leading slash) can be accessed via dictionary index lookup.

The PdfReader object is a subclass of PdfDict, which allows easy access to an entire document:

```
>>> from pdfrw import PdfReader
>>> x = PdfReader('source.pdf')
>>> x.keys()
['/indirect_objects', '/Info', '/Size', '/Root', '/pages']
>>> x.Info
{'/Producer': '(cairo 1.8.6 (http://cairographics.org))',
 '/Creator': '(cairo 1.8.6 (http://cairographics.org))'}
```

indirect\_objects and pages are internally generated, while Info, Size, and Root are retrieved from the trailer of the PDF file.  The only real use for indirect\_objects
is to do debugging.

pages, however, is possibly the most useful attribute of the PdfReader object.  It is a list of all the pages in the document.  It is created because the PDF format allows arbitrarily complicated nested dictionaries to describe the page order.  Each entry in the pages list is the PdfDict object for one of the pages in the file, in order.

```
>>> len(x.pages)
1
>>> x.pages[0]
{'/Parent': {'/Kids': [{...}], '/Type': '/Pages', '/Count': '1'},
 '/Contents': {'/Length': '11260', '/Filter': None},
 '/Resources': ... (Lots more stuff snipped)
>>> x.pages[0].Contents
{'/Length': '11260', '/Filter': None}
>>> x.pages[0].Contents.stream
'q\n1 1 1 rg /a0 gs\n0 0 0 RG 0.657436
  w\n0 J\n0 j\n[] 0.0 d\n4 M q' ... (Lots more stuff snipped)
```

As you can see, it is quite easy to dig down into a PDF document.  But what about when it's time to write it out?

```
>>> from pdfrw import PdfWriter
>>> y = PdfWriter()
>>> y.addpage(x.pages[0])
>>> y.write('result.pdf')
```

That's all it takes to create a new PDF.  You still need to read the [Adobe PDF reference manual](http://www.adobe.com/devnet/acrobat/pdfs/pdf_reference_1-7.pdf) to figure out what needs to go _into_ the PDF, but at least you don't have to sweat actually building it and getting the file offsets right.