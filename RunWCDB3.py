#!/usr/bin/env python
"""
To run the program
    % python RunWCDB3.py < RunWCDB3.in.xml > RunWCDB3.out.xml
    % chmod ugo+x RunCollatz.py
    % RunWCDB3.py < RunWCDB3.in.xml > RunWCDB3.out.xml

To document the program
    % pydoc -w WCDB3
"""

# -------
# imports
# -------

import sys
from WCDB3 import WCDB3_run

WCDB3_run(sys.stdin, sys.stdout)
