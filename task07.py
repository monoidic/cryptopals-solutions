#!/usr/bin/env python3

import base64
from Crypto.Cipher import AES

key = b'YELLOW SUBMARINE'

with open('7.txt') as fd:
  rawdata = fd.read()
  rawdata = base64.b64decode(rawdata)

cipher = AES.new(key, AES.MODE_ECB)
out = cipher.decrypt(rawdata).decode()
print(out)
