#!/usr/bin/env python3

#from Crypto.Cipher import AES

# TODO: ff class?

class Mybytes(bytes):
  def __xor__(self, arg):
    if not isinstance(arg, bytes):
      raise TypeError(f'{arg} is not of a bytes type')
    if len(self) != len(arg):
      raise ValuError('unmatching lengths')

    out = []
    for i in range(len(arg)):
      out.append(self[i] ^ arg[i])
    return Mybytes(out)

  def __add__(self, arg):
    return Mybytes(super().__add__(arg))

  def __getitem__(self, arg):
    if isinstance(arg, int):
      return super().__getitem__(arg)
    return Mybytes(super().__getitem__(arg))

def ff_div(a, mod):
  return ff_divmod(a, mod)[0]

def ff_mod(a, mod):
  return ff_divmod(a,mod)[1]

def ff_divmod(a, mod):
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

def galois_mult(in1, in2, mod=0x11b):
  assert type(in1) == type(in2) == type(mod) == int
  assert in1 >= 0 and in2 >= 0

  out = 0
  mult = 0
  while in1 != 0:
    if in1 & 1:
      out ^= in2 << mult
    in1 >>= 1
    mult += 1

  return ff_mod(out, mod)

def ff_reverse(a):
  assert type(a) == int and a in range(0x100)
  t, t1 = 1, 0
  s, s1 = 0, 1
  r, r1 = a, 0x11b
  while r != 0:
    q = ff_div(r1, r)
    r1, r = r, r1 ^ galois_mult(r, q, 0x200)
    s1, s = s, s1 ^ galois_mult(s, q, 0x200)
    t1, t = t, t1 ^ galois_mult(t, q, 0x200)
  return t1

def circular_shift(value, shift, size=None, lshift=True):
  # value: int or bytes, shift (int, n of bits for int, n of bytes for bytes),
  # size (int, unneeded for bytes, in bits for int), lshift=False for rshift
  assert type(shift) == int
  assert isinstance(value, bytes) or (type(value) == type(size) == int)

  if isinstance(value, bytes):
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

def rcon(i):
  assert type(i) == int
  return Mybytes(int.to_bytes(ff_mod(1 << (i-1), 0x11b), 4, 'little'))

def SubBytes(inbytes, reverse=False):
  assert isinstance(inbytes, bytes)
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
  return Mybytes(out)

def gen_keys(key):	#only AES-128 atm
  N = 4 # n of 32-bit words per key
  R = 11 # n of rounds
  assert isinstance(key, bytes) and len(key) == 4*N

  SubWord = SubBytes
  RotWord = lambda x: circular_shift(x, 1)
  outwords = []
  for i in range(0, 4*N, 4): # first round key == input key
    outwords.append(key[i:i+4])
  for i in range(4, N*R): # other round keys
    word = Mybytes(outwords[i-N])
    if i % N == 0:
      word ^= SubWord(RotWord(outwords[i-1]))
      word ^= rcon(i // N)
    else:
      word ^= outwords[i-1]
    outwords.append(word)
  out = []
  for i in range(0, len(outwords), N): # combine 32-bit words into full keys
    ikey = Mybytes()
    for j in range(N):
      ikey += outwords[i+j]
    out.append(ikey)
  return out

def ShiftRows(inbytes, reverse=False):
  assert isinstance(inbytes, bytes) and len(inbytes) == 16
  out = Mybytes()
  for i in range(4):
    out += circular_shift(inbytes[i*4:(i+1)*4], i, lshift=(not reverse))
  return Mybytes(out)

def MixColumn(b, reverse=False): # TODO: reorder m?
  assert isinstance(b, bytes) and len(b) == 4

  out = []
  if reverse:
    m = [14, 9, 13, 11]
  else:
    m = [2, 1, 1, 3]

  for i in range(4):
    d = 0
    for j in range(4):
      d ^= galois_mult(m[(i-j)%4], b[j])
    out.append(d)
  return Mybytes(out)


def MixColumns(inbytes, reverse=False):
  assert isinstance(inbytes, bytes) and len(inbytes) == 16

  outrows = ( [], [], [], [] )
  for i in range(4):
    column = Mybytes([inbytes[i], inbytes[i+4], inbytes[i+8], inbytes[i+12]])
    column = MixColumn(column, reverse)
    for j in range(4):
      outrows[j].append(column[j])

  out = []
  for row in outrows:
    out += row

  return Mybytes(out)

def aes128_ecb_enc(key, block):		#TODO: doesn't work lol
  assert isinstance(key, bytes) and isinstance(block, bytes)
  assert len(key) == len(block) == 16

  keys = gen_keys(key)
  state = keys[0] ^ block
  for i in range(1, 10):
    state = SubBytes(state)
    state = ShiftRows(state)
    state = MixColumns(state)
    state ^= keys[i]

  state = SubBytes(state)
  state = ShiftRows(state)
  state ^= keys[10]
  return state


def myaesenc(key, plaintext):	#TODO: test after writing aes128_ecb_enc
  assert type(key) == type(plaintext) == bytes
  assert len(key) == 16 and len(plaintext) % 16 == 0

  out = Mybytes()
  for i in range(0, len(plaintext), 16):
    out += aes128_ecb_enc(key, plaintext[i:i+16])
  return out

def myaesdec(key, ciphertext):	#TODO: actually write it lol (then test)
  assert isinstance(key, bytes) and isinstance(ciphertext, bytes)
  pass


if __name__ == '__main__':
  import base64
  key = b'YELLOW SUBMARINE'

  with open('7.txt') as fd:
    rawdata = fd.read()
  rawdata = base64.b64decode(rawdata)

#  cipher = AES.new(key, AES.MODE_ECB)
#  out = cipher.decrypt(rawdata).decode()
#  print(out)
