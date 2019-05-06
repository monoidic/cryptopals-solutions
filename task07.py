#!/usr/bin/env python3

import base64
#from Crypto.Cipher import AES

def euclid_div(a, mod):
  return _euclid_divmod(a, mod)[0]

def euclid_mod(a, mod):
  return _euclid_divmod(a,mod)[1]

def _euclid_divmod(a, mod):
  assert type(a) == type(mod) == int
  bit = a.bit_length() - 1
  modlength = mod.bit_length() - 1
  div = 0
  while bit >= modlength:
    if a & (1 << bit):
      diff = bit - modlength
      div += 1 << diff
      a ^= mod << diff
    bit -= 1
  return (div, a)


#def bezout_identity(a, b):
#  assert type(a) == type(b) == int
#  r, r1 = b, a
#  s, s1 = 0, 1
#  t, t1 = 1, 0
#  while r != 0:
#    q = r1 // r
#    r1, r = r, r1 % r
#    s1, s = s, s1 - q * s
#    t1, t = t, t1 - q * t
#  return (s1, t1)

def ff_reverse(a, mod=0x11b):
  assert type(a) == type(mod) == int
  t, t1 = 1, 0
  s, s1 = 0, 1
  r, r1 = a, mod
  while r != 0:
    q = euclid_div(r1, r)
    r1, r = r, r1 ^ galois_mult(r, q, 0x200)
    s1, s = s, s1 ^ galois_mult(s, q, 0x200)
    t1, t = t, t1 ^ galois_mult(t, q, 0x200)
  return t1

def circular_shift(value, shift, size=None, lshift=True):
  # value: int or bytes, shift (int, n of bits for int, n of bytes for bytes),
  # size (int, unneeded for bytes, in bits for int), lshift=False for rshift
  assert type(shift) == int
  assert type(value) == bytes or (type(value) == type(size) == int)

  if type(value) == bytes:
    size = len(value)
    if not lshift:
      shift = size - shift
    shift %= size
    return value[shift:] + value[:shift]


  assert value < (1 << size)
  shift %= size
  mask = (1 << shift) - 1
  offset = (size - mask.bit_length()) % size
  if lshift:
    mask <<= offset
  mask &= value
  if lshift:
    return ((value << shift) % (1 << size)) ^ (mask >> offset)
  return (value >> shift) ^ (mask << offset)

def galois_mult(in1, in2, mod=0x11b):
  assert type(in1) == type(in2) == type(mod) == int

  out = 0
  mult = 0
  while in1 > 0:
    if in1 & 1:
      out ^= in2 << mult
    in1 >>= 1
    mult += 1

  return euclid_mod(out, mod)


def SubBytes(inbytes, reverse=False):
  assert type(inbytes) == bytes
  out = b''
  if reverse:
    for i in inbytes:
      b = circular_shift(i, 1, 8) ^ circular_shift(i, 3, 8) ^ circular_shift(i, 6, 8) ^ 0x5
      out += bytes([ff_reverse(b)])
  else:
    for i in inbytes:
      b = ff_reverse(i)
      s = b ^ 0x63
      for j in range(1, 5):
        s ^= circular_shift(b, j, 8)
      out += bytes([s])
  return out


def ShiftRow(inbytes):
  assert type(inbytes) == bytes
  out = b''
  for i in range(4):
    out += circular_shift(inbytes[i*4:(i+1)*4], i)
  return out

def MixColumn(inbytes):
  assert type(inbytes) == bytes and len(inbytes) == 4

  mult_column = []

  for i in range(4):
    mult_column.append((inbytes[i] << 1) & 0xff)
    if inbytes[i] & 0x80:
      mult_column[i] ^= 0x1b

  out = []
  for i in range(4):
    out.append(inbytes[(i+1)%4] ^ inbytes[(i+2)%4] ^ inbytes[(i+3)%4] ^ mult_column[i] ^ mult_column[(i+1)%4])
  return bytes(out)

def MixColumns(inbytes):
  assert type(inbytes) == bytes and len(inbytes) == 16

  outrows = [ [] ] * 4
  for i in range(4):
    column = [inbytes[i], inbytes[i+4], inbytes[i+8], inbytes[i+12]]
    mixedcolumn = MixColumn(column)
    for j in range(4):
      outrows[j].append(mixedcolumn[j])

  out = b''
  for row in outrows:
    out += bytes(row)

  return out


def myaesenc(key, plaintext):	#TODO: actually write it lol
  assert type(key) == type(plaintext) == bytes
  pass

def myaesdec(key, ciphertext):	#TODO: actually write it lol
  assert type(key) == type(ciphertext) == bytes
  pass


if __name__ == '__main__':
  key = b'YELLOW SUBMARINE'

  with open('7.txt') as fd:
    rawdata = fd.read()
    rawdata = base64.b64decode(rawdata)

#  cipher = AES.new(key, AES.MODE_ECB)
#  out = cipher.decrypt(rawdata).decode()
#  print(out)
