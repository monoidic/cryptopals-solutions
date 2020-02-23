#!/usr/bin/env python3

import sys
from mystuff import hex_to_b64

# in:
# 49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d

# out:
# SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t
# (I'm killing your brain like a poisonous mushroom)

if len(sys.argv) != 2:
  print('Enter one string of input')
  exit(1)
print(hex_to_b64(sys.argv[1]).decode())
