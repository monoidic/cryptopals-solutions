#!/usr/bin/env python3

from Crypto.Hash import MD5

def hmac_md5(key, plain):
  assert type(key) == type(plain) == bytes

  if len(key) > MD5.block_size:
    key = MD5.MD5Hash(key).digest()
  if len(key) < MD5.block_size:
    key += bytes(MD5.block_size - len(key))

  i_pad, o_pad = b'', b''
  for i in range(MD5.block_size):
    i_pad += bytes([key[i] ^ 0x36])
    o_pad += bytes([key[i] ^ 0x5c])

  sum1 = MD5.MD5Hash(i_pad + plain).digest()
  sum2 = MD5.MD5Hash(o_pad + sum1).digest()

  return sum2.hex()


mykey = b'key'
myplain = b'The quick brown fox jumps over the lazy dog'
#mykey, myplain = b'', b''

print(hmac_md5(mykey, myplain))
