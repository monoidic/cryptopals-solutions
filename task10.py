#!/usr/bin/env python3

import base64, sys, task02
from Crypto.Cipher import AES

def my_cbc(indata, key, IV):
  assert type(indata) == type(key) == type(IV) == bytes
  cipher = AES.new(key, AES.MODE_ECB)
  plain = bytes()
  for i in range(len(indata) // len(key)):
    cipherblock = rawdata[i*len(key):(i+1)*len(key)]
    preplain = cipher.decrypt(cipherblock)
    plain += task02.xor_2_bytes(preplain, IV)
    IV = cipherblock
  return plain

def depkcs7(indata):
  assert type(indata) == bytes
  num = indata[-1]
  if indata[-num:] == bytes([num]) * num:
    return indata[:-num]
  return indata


if __name__ == '__main__':
  key, zeroes_IV = b'YELLOW SUBMARINE', bytes(16) #????
  with open('10.txt') as fd:
    rawdata = fd.read()
    rawdata = base64.b64decode(rawdata)
  plain = my_cbc(rawdata, key, zeroes_IV)
  plain = depkcs7(plain)
  print(plain)
