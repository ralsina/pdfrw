## Introduction ##

The [pdfrw library](http://code.google.com/p/pdfrw/source/browse/trunk/pdfrw/) currently consists of 16 modules organized into a main package and one sub-package.

The [\_\_init\_\_.py](http://code.google.com/p/pdfrw/source/browse/trunk/pdfrw/__init__.py) module does the usual thing of importing a few major attributes from some of the submodules, and the [errors.py](http://code.google.com/p/pdfrw/source/browse/trunk/pdfrw/errors.py) module supports logging and exception generation.

## PDF ObjectModel support ##

The [objects sub-package](http://code.google.com/p/pdfrw/source/browse/trunk/pdfrw/objects/) contains files (and corresponding modules) for each of the internal representations of the kinds of basic objects that exist in a PDF file, with the [objects/\_\_init\_\_.py](http://code.google.com/p/pdfrw/source/browse/trunk/pdfrw/objects/__init__.py) in that module simply gathering them up and making them available to the main pdfrw package.

One feature that all the PDF object classes have in common is the inclusion of an 'indirect' attribute.  If 'indirect' exists and evaluates to True, then when the object is written out, it is written out as an indirect object.  That is to say, it is addressable in the PDF file, and could be referenced by any number (including zero) of container objects.  This indirect object capability allows PDF files to contain internal circular references.

### Ordinary objects ###

The [objects/pdfobject.py](http://code.google.com/p/pdfrw/source/browse/trunk/pdfrw/objects/pdfobject.py) module contains the PdfObject class, which is a subclass of str.  Any PDF object except the container objects (PdfArray and PdfDict) could be represented by a PdfObject (or a regular string, for that matter), but PDF "string" objects are typically represented separately to distinguish encoded from unencoded strings.

### Name objects ###

The [objects/pdfname.py](http://code.google.com/p/pdfrw/source/browse/trunk/pdfrw/objects/pdfname.py) module contains the PdfName singleton object, which will convert a string into a PDF name by prepending a slash.  It can be used either by calling it or getting an attribute, e.g.:
```
        PdfName.Rotate == PdfName('Rotate') == PdfObject('/Rotate')
```
Currently, this only works with names that don't need to be encoded (that don't incorporate special PDF file characters such as whitespace or delimiters).

### String objects ###

The [objects/pdfstring.py](http://code.google.com/p/pdfrw/source/browse/trunk/pdfrw/objects/pdfstring.py) module contains the PdfString class, which is a subclass of str that is used to represent encoded strings in a PDF file.  The class has encode and decode methods for the strings.

### Array objects ###

The [objects/pdfarray.py](http://code.google.com/p/pdfrw/source/browse/trunk/pdfrw/objects/pdfstring.py) module contains the PdfArray class, which is a subclass of list that is used to represent arrays in a PDF file.  A regular list could be used instead, but use of the PdfArray class allows for an indirect attribute to be set, and also allows for proxying of unresolved indirect objects (that haven't been read in yet) in a manner that is transparent to pdfrw clients.

### Dict objects ###

The [objects/pdfdict.py](http://code.google.com/p/pdfrw/source/browse/trunk/pdfrw/objects/pdfdict.py) module contains the PdfDict class, which is a subclass of dict that is used to represent dictionaries in a PDF file.  A regular dict could be used instead, but use of the PdfDict class allows for many ease of use features:
  * Transparent (from the library client's viewpoint) proxying of unresolved indirect objects
  * Return of None for non-existent keys (like dict.get)
  * Mapping of attribute accesses to the dict itself (pdfdict.Foo == pdfdict['/Foo'])
  * Automatic management of following stream and /Length attributes for content dictionaries
  * Indirect attribute
  * Other attributes may be set for private internal use of the library and/or its clients.

### Proxy objects ###

The [objects/pdfindirect.py](http://code.google.com/p/pdfrw/source/browse/trunk/pdfrw/objects/pdfindirect.py) module contains the PdfIndirect class, which is a non-transparent proxy object for PDF objects that have not yet been read in and resolved from a file.  Client code should never see one of these -- they exist inside the PdfArray and PdfDict container types, but are resolved before being returned to a client of those types.

## File reading, tokenization and parsing ##

[pdfreader.py](http://code.google.com/p/pdfrw/source/browse/trunk/pdfrw/pdfreader.py) contains the PdfReader class, which can read a PDF file (or be passed a file object or already read string) and parse it.  It uses the PdfTokens class in [tokens.py](http://code.google.com/p/pdfrw/source/browse/trunk/pdfrw/tokens.py) for low-level tokenization.

The PdfReader class does not, in general, parse into containers (e.g. inside the content streams).  There is a proof of concept for doing that inside the examples/rl2 subdirectory, but that is slow and not useful for most applications.

## File output ##

[pdfwriter.py](http://code.google.com/p/pdfrw/source/browse/trunk/pdfrw/pdfwriter.py) contains the PdfWriter class, which can create and output a PDF file.

## Advanced features ##

[compress.py](http://code.google.com/p/pdfrw/source/browse/trunk/pdfrw/compress.py) and  [uncompress.py](http://code.google.com/p/pdfrw/source/browse/trunk/pdfrw/uncompress.py) contains compression and decompression functions.  Very few filters are currently supported, so an external tool like pdftk might be good if you require the ability to decompress (or, for that matter, decrypt) PDF files.

[buildxobj.py](http://code.google.com/p/pdfrw/source/browse/trunk/pdfrw/buildxobj.py) contains functions to build FormXObjects out of pages or rectangles on pages.

[toreportlab.py](http://code.google.com/p/pdfrw/source/browse/trunk/pdfrw/toreportlab.py) provides the makerl function, which will translate pdfrw objects into a format which can be used with [reportlab](http://www.reportlab.org/).  It is normally used in conjunction with buildxobj, to be able to reuse parts of existing PDFs when using reportlab.