# A part of pdfrw (pdfrw.googlecode.com)
# Copyright (C) 2006-2009 Patrick Maupin, Austin, Texas
# MIT license -- See LICENSE.txt for details

from pdfwriter import PdfWriter
from pdfreader import PdfReader
from pdfobjects import PdfObject, PdfName, PdfArray, PdfDict, IndirectPdfDict, PdfString
from new_pdftokens import PdfTokens
from pdferrors import PdfParseError

# Add a tiny bit of compatibility to pyPdf

PdfFileReader = PdfReader
PdfFileWriter = PdfWriter