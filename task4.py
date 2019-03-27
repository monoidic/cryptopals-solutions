#!/usr/bin/env python3

import task3

# out:
# Now that the party is jumping\n

#def flatten(inlist):
#  assert type(inlist) == list
#  return [item for sublist in inlist for item in sublist]

if __name__ == '__main__':
  maybes = list()
  with open('4.txt') as fd:
    for line in fd:
      linebytes = bytes.fromhex(line)
      pr_list = task3.get_printables(linebytes)
      if pr_list:
        maybes += pr_list[:5]
  likely = task3.least_symbols(maybes)
  print(likely)
