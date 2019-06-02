#!/usr/bin/env python3

import base64

def hex_to_b64(instr):
  return base64.b64encode(bytes.fromhex(instr))

def xor_2_bytes(in1, in2):
  assert len(in1) == len(in2)
  out = b''
  for i in range(len(in1)):
    out += bytes([in1[i] ^ in2[i]])
  return out

def printable(inbytes):
  assert type(inbytes) == bytes

  if not inbytes.isascii():
    return False

  for ranges in range(0x9), range(0xb, 0x20):
    for i in ranges:
      if inbytes.find(bytes([i])) != -1:
        return False
  return True

def printsort(inlist, rev=False):
  return sorted(inlist, key=lambda x: return x[0], reverse=rev)

def least_symbols(inlist):
  assert type(inlist) == list

  inter = []
  for ilist in inlist:
    specialcount = 0
    for ranges in range(0x21, 0x30), range(0x3a, 0x41), range(0x5b, 0x61), \
    range(0x7b, 0x80):
      for i in ranges:
        specialcount_t = ilist.count(i)
        if specialcount_t != -1:
          specialcount += specialcount_t
    inter.append(tuple([specialcount, ilist]))
  inter = printsort(inter)
#  for i in inter:
#    out.append(i[1])
#  return out
  return inter[0][1]

def get_printables(inbytes):
  out = list()
  for i in range(0x100):
    xor_bytes = bytes([i]) * len(inbytes)
    maybe_p = xor_2_bytes(inbytes, xor_bytes)
    if printable(maybe_p):
      out.append(maybe_p)
  return out

def repeating_key_xor(inbytes, key):
  inlen, keylen = len(inbytes), len(key)
  out = []
  for i in range(inlen):
#    out += bytes([inbytes[i] ^ key[i%keylen]])
    out.append(inbytes[i] ^ key[i%keylen])
  return bytes(out)

def least_symbols_printable(inbytes):
  return least_symbols(get_printables(inbytes))

def hamming_bits(in1, in2):
  if type(in1) == type(in2) == bytes:
    assert len(in1) == len(in2)
    in1 = int.from_bytes(in1, 'big')
    in2 = int.from_bytes(in1, 'big')
  assert type(in1) == type(in2) == int

#  diff = in1 ^ in2
#  out = 0
#  while diff:
#    out += diff & 1
#    diff >>= 1
  return f'{in1 ^ in2:b}'.count('1')
#  return out

def find_keysize(input):
  assert type(input) == bytes
  assert len(input) >= 800

  hamming_results = []
  for keysize in range(2, 40):
    result = 0
    for i in range(keysize):
      for j in range(20):
        result += hamming_bits(input[keysize*j + i], input[keysize*(j+1) + i])
    hamming_results.append(tuple([result / keysize, keysize]))
#  return hamming_results
  return printsort(hamming_results)[0][1]
