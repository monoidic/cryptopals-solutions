#!/usr/bin/env python3

import task07

for i in range(1, 256):
  x = task07.ff_reverse(i)
  if task07.galois_mult(x, i) != 1:
    print(i)
