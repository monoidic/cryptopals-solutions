#!/usr/bin/env python3

import sys
from mystuff import xor_2_bytes

# in:
# 1c0111001f010100061a024b53535009181c  686974207468652062756c6c277320657965

# out:
# 746865206b696420646f6e277420706c6179
# (the kid don't play)

if len(sys.argv) != 3:
  print('Enter 2 strings of input')
  exit(1)
x1, x2 = bytes.fromhex(sys.argv[1]), bytes.fromhex(sys.argv[2])
print(xor_2_bytes(x1, x2).hex())
