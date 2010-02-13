# A part of pdfrw (pdfrw.googlecode.com)
# Copyright (C) 2006-2009 Patrick Maupin, Austin, Texas
# MIT license -- See LICENSE.txt for details

'''
A tokenizer for PDF streams.

In general, documentation used was "PDF reference",
sixth edition, for PDF version 1.7, dated November 2006.

'''

from __future__ import generators
from sets import Set as set
import re
from pdfobjects import PdfString, PdfObject

class _PrimitiveTokens(object):

    # Table 3.1, page 50 of reference, defines whitespace
    whitespaceset = set('\x00\t\n\f\r ')


    # Text on page 50 defines delimiter characters
    delimiterset = set('()<>{}[]/%')

    # Coalesce contiguous whitespace into a single token
    whitespace_pattern = '[%s]+' % ''.join(whitespaceset)

    # In addition to the delimiters, we also use '\', which
    # is special in some contexts in PDF.
    delimiter_pattern = '\\\\|\\' + '|\\'.join(delimiterset)

    # Dictionary delimiters are '<<' and '>>'.  Look for
    # these before the single variety.
    dictdelim_pattern = r'\<\<|\>\>'

    pattern = '(%s|%s|%s)' % (whitespace_pattern,
                    dictdelim_pattern, delimiter_pattern)
    re_func = re.compile(pattern).finditer
    del whitespace_pattern, dictdelim_pattern
    del delimiter_pattern, pattern

    def __init__(self, fdata, startloc):

        class MyIterator(object):
            def next():
                if not tokens:
                    startloc = self.startloc
                    match = next_match()
                    if match is not None:
                        start = match.start()
                        end = match.end()
                        tokens.append(fdata[start:end])
                        if start > startloc:
                            tokens.append(fdata[startloc:start])
                        self.startloc = end
                    else:
                        s = fdata[startloc:]
                        if s:
                            tokens.append(s)
                    if not tokens:
                        raise StopIteration
                return tokens.pop()
            next = staticmethod(next)

        next_match = self.re_func(fdata, startloc).next
        self.fdata = fdata
        self.startloc = startloc
        self.tokens = tokens = []
        self.iterator = iterator = MyIterator()
        self.next = iterator.next

    def __iter__(self):
        return self.iterator

    def coalesce(self, result):
        ''' This function coalesces tokens together up until
            the next delimiter or whitespace.
            All of the coalesced tokens will either be non-matches,
            or will be a matched backslash.  We distinguish the
            non-matches by the fact that next() will have left
            a following match inside self.tokens.
        '''
        tokens = self.tokens
        for token in self:
            # If it is a non-match or a backslash, take it
            if tokens or token == '\\':
                result.append(token)
            else:
                # push it back for next time and get out
                tokens.append(token)
                return

    def floc(self):
        return self.startloc - sum([len(x) for x in self.tokens])

class PdfTokens(object):

    def __init__(self, fdata, startloc=0, strip_comments=True):

        def comment(token):
            tokens = [token]
            for token in primitive:
                tokens.append(token)
                if token[0] in whitespaceset and ('\n' in token or '\r' in token):
                    break
            return not strip_comments and ''.join(tokens)

        def single(token):
            return token

        def regular_string(token):
            def escaped():
                escaped = False
                i = -2
                while tokens[i] == '\\':
                    escaped = not escaped
                    i -= 1
                return escaped

            tokens = [token]
            nestlevel = 1
            for token in primitive:
                tokens.append(token)
                if token in '()' and not escaped():
                    nestlevel += token == '(' or -1
                    if not nestlevel:
                        break
            else:
                assert 0, "Unexpected end of token stream"
            return PdfString(''.join(tokens))

        def hex_string(token):
            tokens = [token]
            for token in primitive:
                tokens.append(token)
                if token == '>':
                    break
            while tokens[-2] == '>>':
                tokens.append(tokens.pop(-2))
            return PdfString(''.join(tokens))

        def normal_data(token):
            if token[0] in whitespaceset:
                return
            tokens = [token]
            primitive.coalesce(tokens)
            return PdfObject(''.join(tokens))

        def name_string(token):
            tokens = [token]
            primitive.coalesce(tokens)
            token = ''.join(tokens)
            if '#' in token:
                substrs = token.split('#')
                substrs.reverse()
                tokens = [substrs.pop()]
                while substrs:
                    s = substrs.pop()
                    tokens.append(chr(int(s[:2], 16)))
                    tokens.append(s[2:])
                token = ''.join(tokens)
            return PdfObject(token)

        def broken(token):
            assert 0, token

        dispatch = {
            '(': regular_string,
            ')': broken,
            '<': hex_string,
            '>': broken,
            '[': single,
            ']': single,
            '{': single,
            '}': single,
            '/': name_string,
            '%' : comment,
            '<<': single,
            '>>': single,
        }.get

        class MyIterator(object):
            def next():
                while not tokens:
                    token = primitive_next()
                    token = dispatch(token, normal_data)(token)
                    if token:
                        return token
                return tokens.pop()
            next = staticmethod(next)

        self.primitive = primitive = _PrimitiveTokens(fdata, startloc)
        self.fdata = fdata
        self.strip_comments = strip_comments
        self.tokens = tokens = []
        whitespaceset = _PrimitiveTokens.whitespaceset
        self.iterator = iterator = MyIterator()
        self.next = iterator.next
        primitive_next = primitive.next

    def floc(self):
        return self.primitive.floc() - sum([len(x) for x in self.tokens])
    floc = property(floc)

    def __iter__(self):
        return self.iterator

    def multiple(self, count):
        next = self.next
        return [next() for i in range(count)]