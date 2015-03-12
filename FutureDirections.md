# Introduction #

This page details, in a very uneven level of specificity, work to be done.


# Support for encryption #

Some PDFs are encrypted.  I don't really care, but I might if someone paid me enough.

# Support for more compression filters #

Some PDFs need to be decompressed for some operations.  For the most part, for most things, this works fine right now, because a lot of useful things can be done without compressing or decompressing.  Am planning on adding support for /Flate decompression with the PNG predictor options.

# Support for version 1.15 compressed object streams and compressed xref streams #

Currently, I plan to implement these for reading.  No current plans for writing.

# New "mashup" functions #

Am considering putting a lot of the functionality of the example programs in a "mashup" subpackage that understands how to create documents from multiple PDFs.  That and a single program to drive it would be excellent as a standalone program, and also as a demonstration of the capabilities.