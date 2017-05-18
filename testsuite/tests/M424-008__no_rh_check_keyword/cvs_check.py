#! /usr/bin/env python
"""A dummy cvs_check program that passes all files.

It also prints a trace on stdout, in order to allow us to allow us
to verify that the script was called with the correct arguments.
"""
import sys

# To help with testing, print a trace containing the name of the module
# and the name of the file being checked.
print "cvs_check: `%s' `%s'" % (sys.argv[1], sys.argv[2])

if sys.argv[2] == 'b':
    print "*** cvs_check: some style errors in: %s" % sys.argv[2]
    sys.exit(1)
