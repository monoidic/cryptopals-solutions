#!/usr/bin/env python3

linecounter = 1
found = False
with open('8.txt') as fd:
  while True:
    line = fd.readline()
    if not line:
      break
    rawline = bytes.fromhex(line)
    myset = set()
    for i in range(4):
      myset.add(rawline[i*16:(i+1)*16])
    if 4 != len(myset):
      found = True
      break
    linecounter += 1

if found:
  print(f'The line encrypted with ECB is line {linecounter}')
  print('It contained to following:')
  print(line)
