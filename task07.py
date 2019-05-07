#!/usr/bin/env python3

import base64
#from Crypto.Cipher import AES

#TODO: key schedule

def xor_bytes(inb1, inb2):
  assert type(inb1) == type(inb2) == bytes
  assert len(inb1) == len(inb2)
  out = []
  for i in range(len(inb1)):
    out.append(inb1[i] ^ inb2[i])
  return bytes(out)

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

def ff_reverse(a, mod=0x11b):
  assert type(a) == type(mod) == int and a in range(0x100)
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
  offset = (size - shift) % size
  if lshift:
    mask = ((mask << offset) & value) >> offset
    unmasked = (value << shift) % (1 << size)
  else:
    mask = (mask & value) << offset
    unmasked = value >> shift
  return mask ^ unmasked

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

def roundconst(i):
  assert type(i) == int
  return int.to_bytes(euclid_mod(1 << (i-1), 0x11b), 4, 'little')

def gen_keys(key):	#only AES-128 atm
  assert type(key) == bytes and len(key) == 16
  outwords = []
  for i in range(0, 16, 4):
    outwords.append(key[i:i+4])
  for i in range(4, 44):
    word = outwords[i-4]
    if i % 4 == 0:
      word = xor_bytes(SubBytes(circular_shift(outwords[i-1], 1)), word)
      word = xor_bytes(roundconst(i // 4), word)
    else:
      word = xor_bytes(outwords[i-1], word)
    outwords.append(word)
  out = []
  for i in range(0, len(outwords), 4):
    out.append(outwords[i] + outwords[i+1] + outwords[i+2] + outwords[i+3])
  return out


def SubBytes(inbytes, reverse=False):
  assert type(inbytes) == bytes
  out = []
  if reverse:
    for i in inbytes:
      b = circular_shift(i, 1, 8) ^ circular_shift(i, 3, 8) ^ circular_shift(i, 6, 8) ^ 0x5
      out.append(ff_reverse(b))
  else:
    for i in inbytes:
      b = ff_reverse(i)
      s = b ^ 0x63
      for j in range(1, 5):
        s ^= circular_shift(b, j, 8)
      out.append(s)
  return bytes(out)


def ShiftRows(inbytes, reverse=False):
  assert type(inbytes) == bytes and len(inbytes) == 16
  out = b''
  for i in range(4):
    out += circular_shift(inbytes[i*4:(i+1)*4], i, not reverse)
  return out

def MixColumn(b, reverse=False):
  assert type(b) == bytes and len(b) == 4

  out = []
  if reverse:
    m = [14, 9, 13, 11]
  else:
    m = [2, 1, 1, 3]

  for i in range(4):
    d = galois_mult(m[i], b[0]) ^ galois_mult(m[(i+3)%4], b[1])
    d ^= galois_mult(m[(i+2)%4], b[2]) ^ galois_mult(m[(i+1)%4], b[3])
    out.append(d)
  return bytes(out)


def MixColumns(inbytes, reverse=False):
  assert type(inbytes) == bytes and len(inbytes) == 16

  outrows = [ [], [], [], [] ]
  for i in range(4):
    column = bytes([inbytes[i], inbytes[i+4], inbytes[i+8], inbytes[i+12]])
    column = MixColumn(column, reverse)
    for j in range(4):
      outrows[j].append(column[j])

  out = []
  for row in outrows:
    out += row

  return bytes(out)

def aes128_ecb_enc(key, block):
  assert type(key) == type(block) == bytes
  assert len(key) == len(block) == 16

  keys = gen_keys(key)
  state = xor_bytes(keys[0], block)
  for i in range(1, 10):
    state = SubBytes(state)
    state = ShiftRows(state)
    state = MixColumns(state)
    state = xor_bytes(keys[i], state)

  state = SubBytes(state)
  state = ShiftRows(state)
  state = xor_bytes(keys[10], state)
  return state


def myaesenc(key, plaintext):	#TODO: actually write it lol
  assert type(key) == type(plaintext) == bytes
  assert len(key) == 16 and len(plaintext) % 16 == 0

  out = b''
  for i in range(0, len(plaintext), 16):
    out += aes128_ecb_enc(key, plaintext[i:i+16])
  return out

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
