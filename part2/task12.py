#!/usr/bin/env python3

import mystuff
import base64, os

mystery = base64.b64decode('Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK')

_key = os.urandom(16)

def encrypt_oracle(input):
  assert type(input) == bytes
  input = mystuff.pkcs7_pad(input + mystery, len(_key))
  return mystuff.my_ecb_enc(input, _key)

def get_blocksize(fun):
  initial_size = len(fun(b''))
  for i in range(1, 65):
    outlen = len(fun(b'A'*i))
    if outlen == initial_size:
      continue
    return outlen - initial_size
  raise Exception("Block size didn't change? (or bs > 512 bits)")

def detect_ecb(fun, blocksize): # assumes no prefix for simplicity - could also insert 3 blocks, then look for 2 contiguous identical blocks across all input
  input = b'A' * (blocksize * 2)
  out = fun(input)
  return out[0:blocksize] == out[blocksize:2*blocksize]

def main():
  bs = get_blocksize(encrypt_oracle)
  is_ecb = detect_ecb(encrypt_oracle, bs)
  print(f'Blocksize: {bs}, is ECB: {is_ecb}')

if __name__ == '__main__':
  main()
