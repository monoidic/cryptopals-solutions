#!/usr/bin/env python3

import sys
from mystuff import least_symbols_printable

# in:
# 1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736

# out:
# Cooking MC's like a pound of bacon


if len(sys.argv) != 2:
  print('Enter 1 string of input')
  exit(1)

out = least_symbols_printable(bytes.fromhex(sys.argv[1]))

print(out.decode())
