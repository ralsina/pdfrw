## Pure Python ##

  * [reportlab](http://www.reportlab.org/)

> reportlab is must-have software if you want to programmatically
> generate arbitrary PDFs.

  * [pyPdf](http://pybrary.net/pyPdf/)

> pyPdf is, in some ways, very full-featured.
> It can do decompression and decryption and seems
> to know a lot about items inside at least some
> kinds of PDF files.  In comparison, pdfrw knows
> less about specific PDF file features (such as
> metadata), but focuses on trying to have a more
> Pythonic API for mapping the PDF file container
> syntax to Python, and (IMO) has a simpler and
> better PDF file parser.

  * [pdftools](http://www.boddie.org.uk/david/Projects/Python/pdftools/index.html)

> pdftools feels large and I fell asleep trying to figure
> out how it all fit together, but many others have
> done useful things with it.

  * [pagecatcher](http://www.reportlab.com/docs/pagecatcher-ds.pdf)

> My understanding is that pagecatcher would have done
> exactly what I wanted when I built pdfrw.  But I was
> on a zero budget, so I've never had the pleasure of
> experiencing pagecatcher.  I do, however, use and
> like [reportlab](http://www.reportlab.org/)
> (open source, from the people who make pagecatcher)
> so I'm sure pagecatcher is great, better documented
> and much more full-featured than the open source
> options.

  * [pdfminer](http://www.unixuser.org/~euske/python/pdfminer/index.html)

> This looks like a useful, actively-developed program.  It is quite
> large, but then, it is trying to actively comprehend a full PDF
> document.  From the website:

> "PDFMiner is a suite of programs that help extracting and analyzing text data of PDF documents. Unlike other PDF-related tools, it allows to obtain the exact location of texts in a page, as well as other extra information such as font information or ruled lines. It includes a PDF converter that can transform PDF files into other text formats (such as HTML). It has an extensible PDF parser that can be used for other purposes instead of text analysis."



## non-pure-Python libraries ##

  * [pyPoppler](https://launchpad.net/poppler-python/) can read PDF files.
  * [pycairo](http://www.cairographics.org/pycairo/) can write PDF files.

## Other tools ##

  * [pdftk](http://www.accesspdf.com/pdftk/) is a wonderful command line tool for basic PDF manipulation.  It complements pdfrw extremely well, supporting many operations such as decryption and decompression that pdfrw cannot do.