#!/usr/bin/env python3

import sys
from mystuff import repeating_key_xor

# in:
# "Burning 'em, if you ain't quick and nimble"$'\n'"I go crazy when I hear a cymbal"
# 'ICE'

# out:
# 0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f

if len(sys.argv) != 3:
  print('Enter plaintext/ciphertext and key')
  exit(1)

plain, key = bytes(sys.argv[1], 'UTF-8'), bytes(sys.argv[2], 'UTF-8')
ciphertext = repeating_key_xor(plain, key)
print(ciphertext.hex())
