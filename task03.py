#!/usr/bin/env python3

import sys, task2, pprint

# in:
# 1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736

# out:
# Cooking MC's like a pound of bacon

def printable(inbytes):
  assert type(inbytes) == bytes

  if not inbytes.isascii():
    return False

  for ranges in range(0x9), range(0xb, 0x20):
    for i in ranges:
      if inbytes.find(int.to_bytes(i, 1, sys.byteorder)) != -1:
        return False
  return True

def tuple_sort(intup):
  return intup[0]

def printsort(inlist, rev=False):
  return sorted(inlist, key=tuple_sort, reverse=rev)

def least_symbols(inlist):
  assert type(inlist) == list

  inter = list()
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
    xor_bytes = int.to_bytes(i, 1, sys.byteorder) * len(inbytes)
    maybe_p = task2.xor_2_bytes(inbytes, xor_bytes)
    if printable(maybe_p):
      out.append(maybe_p)
  return out

def dostuff(inbytes):
  printables = get_printables(inbytes)
#  return least_symbols(printables)[0]
  return least_symbols(printables)


if __name__ == '__main__':
  if len(sys.argv) != 2:
    print('Enter 1 string of input')
    exit(1)

#  pprint.pprint(least_symbols(pr_list)[0])
  print(dostuff(bytes.fromhex(sys.argv[1])).decode())
