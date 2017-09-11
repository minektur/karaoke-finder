#!/usr/bin/env python
""" investigate non-normalized-filenames in corpus"""

import sys

for line in sys.stdin:
    first = line.find("- ")
    second = line.find("-")
    if first != second:
        print(line, end="")
