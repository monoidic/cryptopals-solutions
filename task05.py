#!/usr/bin/env python3

import sys

# in:
# "Burning 'em, if you ain't quick and nimble"$'\n'"I go crazy when I hear a cymbal"
# 'ICE'

# out:
# 0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20
# 430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f


def repeating_key_xor(inbytes, key):
  inlen, keylen = len(inbytes), len(key)
  out = bytes()
  for i in range(inlen):
    out += int.to_bytes(inbytes[i] ^ key[i%keylen], 1, sys.byteorder)
  return out

if __name__ == '__main__':
  if len(sys.argv) != 3:
    print('Enter plaintext/ciphertext and key')
    exit(1)

  plain, key = bytes(sys.argv[1], 'UTF-8'), bytes(sys.argv[2], 'UTF-8')
  ciphertext = repeating_key_xor(plain, key)
  print(ciphertext.hex())
