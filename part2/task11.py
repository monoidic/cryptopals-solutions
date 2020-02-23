#!/usr/bin/env python3

from Crypto.Cipher import AES
import os, random

import mystuff


def encryption_oracle(input):
  prefix = os.urandom(random.randint(5, 10))
  suffix = os.urandom(random.randint(5, 10))
  input = mystuff.pkcs7_pad(prefix + input + suffix, 16)
  key = os.urandom(16)
  if random.getrandbits(1):
    IV = os.urandom(16)
    return ('CBC', mystuff.my_cbc_enc(input, key, IV))
  else:
    return ('ECB', mystuff.my_ecb_enc(input, key))

def guess_encryption(incipher):
  return 'ECB' if incipher[16:32] == incipher[32:48] else 'CBC'

def main():
  input = b'A' * 43 # handles worst case: prefix of 5 (11 eaten by first block), 2 blocks after (32)
  for i in range(1, 11):
    answer, cipher = encryption_oracle(input)
    if guess_encryption(cipher) == answer:
      print(f'Yay, guessed correctly ({i}/10)')
    else:
      print(f'Wrong! ({i}/10)')

if __name__ == '__main__':
  main()
