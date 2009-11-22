# A part of pdfrw (pdfrw.googlecode.com)
# Copyright (C) 2006-2009 Patrick Maupin, Austin, Texas
# MIT license -- See LICENSE.txt for details

'''
Objects that can occur in PDF files.  The most important
objects are arrays and dicts.  Either of these can be
indirect or not, and dicts could have an associated
stream.
'''
import re

class PdfObject(str):
    indirect = False

class PdfArray(list):
    indirect = False

class PdfName(object):
    def __getattr__(self, name):
        return self(name)
    def __call__(self, name):
        return PdfObject('/' + name)

PdfName = PdfName()

class PdfString(str):
    unescape_dict = {'\\b':'\b', '\\f':'\f', '\\n':'\n',
                     '\\r':'\r', '\\t':'\t',
                     '\\\r\n': '', '\\\r':'', '\\\n':'',
                     '\\\\':'\\', '\\':'',
                    }
    unescape_pattern = r'(\\b|\\f|\\n|\\r|\\t|\\\r\n|\\\r|\\\n|\\[0-9]+|\\)'
    unescape_func = re.compile(unescape_pattern).split

    hex_pattern = '([a-fA-F0-9][a-fA-F0-9]|[a-fA-F0-9])'
    hex_func = re.compile(hex_pattern).split

    hex_pattern2 = '([a-fA-F0-9][a-fA-F0-9][a-fA-F0-9][a-fA-F0-9]|[a-fA-F0-9][a-fA-F0-9]|[a-fA-F0-9])'
    hex_func2 = re.compile(hex_pattern2).split

    hex_funcs = hex_func, hex_func2

    indirect = False

    def decode_regular(self, remap=chr):
        assert self[0] == '(' and self[-1] == ')'
        mylist = self.unescape_func(self[1:-1])
        result = []
        unescape = self.unescape_dict.get
        for chunk in mylist:
            chunk = unescape(chunk, chunk)
            if chunk.startswith('\\') and len(chunk) > 1:
                value = int(chunk[1:], 8)
                # FIXME: TODO: Handle unicode here
                if value > 127:
                    value = 127
                chunk = remap(value)
            if chunk:
                result.append(chunk)
        return ''.join(result)

    def decode_hex(self, remap=chr, twobytes=False):
        data = self
        data = self.hex_funcs[twobytes](self)
        chars = data[1::2]
        other = data[0::2]
        assert other[0] == '<' and other[-1] == '>' and ''.join(other) == '<>', self
        return ''.join(remap(int(x, 16)) for x in chars)

    def decode(self, remap=chr, twobytes=False):
        if self.startswith('('):
            return self.decode_regular(remap)

        else:
            return self.decode_hex(remap, twobytes)

class PdfDict(dict):
    indirect = False
    stream = None

    _special = dict(indirect = ('indirect', False),
                    stream = ('stream', True),
                    _stream = ('stream', False),
                   )

    def __init__(self, *args, **kw):
        for key, value in kw.iteritems():
            setattr(self, key, value)
        if args:
            if len(args) == 1:
                args = args[0]
            self.update(args)

    def __getattr__(self, name):
        return self.get(PdfName(name))

    def __setattr__(self, name, value):
        info = self._special.get(name)
        if info is None:
            self[PdfName(name)] = value
        else:
            name, setlen = info
            self.__dict__[name] = value
            if setlen:
                notnone = value is not None
                self.Length = notnone and PdfObject(len(value)) or None

    def iteritems(self):
        for key, value in dict.iteritems(self):
            if value is not None:
                assert key.startswith('/'), (key, value)
                yield key, value

class IndirectPdfDict(PdfDict):
    indirect = True