#!/usr/bin/env python3

import sys

def pkcs7_pad(input, blocksize):
  assert type(input) == bytes
  assert type(blocksize) == int and blocksize < 256
  padsize = blocksize % len(input)
  padding = int.to_bytes(padsize, 1, sys.byteorder) * padsize
  return input + padding

if __name__ == '__main__':
  if len(sys.argv) != 3:
    print('Enter input to pad and blocksize (in bytes)')
    exit(1)
  myin, mybs = bytes(sys.argv[1], 'UTF-8'), int(sys.argv[2])
  out = pkcs7_pad(myin, mybs)
  print(out)
