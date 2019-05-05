#!/usr/bin/env python3

from mystuff import get_printables, least_symbols

# out:
# Now that the party is jumping\n

#def flatten(inlist):
#  assert type(inlist) == list
#  return [item for sublist in inlist for item in sublist]

maybes = list()
with open('4.txt') as fd:
  for line in fd:
    linebytes = bytes.fromhex(line)
    pr_list = get_printables(linebytes)
    if pr_list:
      maybes += pr_list[:5]
likely = least_symbols(maybes)
print(likely)
