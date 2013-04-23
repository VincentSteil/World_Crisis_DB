#!/usr/bin/env python
"""
To run the program
    % python RunWCDB1.py < RunWCDB1.in.xml > RunWCDB1.out.xml
    % chmod ugo+x RunCollatz.py
    % RunWCDB1.py < RunWCDB1.in.xml > RunWCDB1.out.xml

To document the program
    % pydoc -w WCDB1
"""

# -------
# imports
# -------

import sys
from WCDB1 import WCDB1_run

WCDB1_run(sys.stdin, sys.stdout)
