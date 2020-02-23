#!/usr/bin/env python3

# key: b'Terminator X: Bring the noise' (not sticking the full output here)

from mystuff import printsort, find_keysize

if __name__ == '__main__':
  import base64, sys
  from mystuff import xor_2_bytes, least_symbols_printable

  with open('6.txt') as fd:
    rawdata = fd.read()
    rawdata = base64.b64decode(rawdata)

  keysize = find_keysize(rawdata)
  print(f'Estimated keysize: {keysize}')
  single_xor_chunks = list()
  for i in range(keysize):
    single_xor_chunks.append(bytes())
  for i in range(len(rawdata)):
    single_xor_chunks[i%keysize] += bytes([rawdata[i]])
  solved_chunks = list()
  for item in single_xor_chunks:
    solved_chunks.append(least_symbols_printable(item))
  solved = bytes()
  for i in range(len(rawdata)):
    x, y = i % keysize, i // keysize
    solved += bytes([solved_chunks[x][y]])
  key = xor_2_bytes(rawdata[:keysize], solved[:keysize])
  print(f'Guessed key: {key}\n\n')
  print(solved.decode())


#KEYSIZE = 29
#input_chunks = list()
#with open('6.bin', 'rb') as fd:
#  while True:
#    data = fd.read(KEYSIZE)
#    if not data:
#      break
#    input_chunks.append(data)
#
#single_xor_chunks = list()
#for i in range(KEYSIZE):
#  single_xor_chunks.append(bytes())
#
#for i in input_chunks:
#  for j in range(KEYSIZE):
#    if j >= len(i):
#      continue
#    single_xor_chunks[j] += int.to_bytes(i[j], 1, sys.byteorder)

#pprint.pprint(single_xor_chunks)

#print(task03.dostuff(single_xor_chunks[0]))

#xored_chunks = list()
#for chunk in single_xor_chunks:
#  xored_chunks.append(task03.dostuff(chunk))
#
#out = bytes()
#for i in range(KEYSIZE):
#  for chunk in xored_chunks:
#   if i >= len(chunk):
#     continue
#   out += int.to_bytes(chunk[i], 1, sys.byteorder)
#
#print(out.decode())

#data = bytes()
#with open('6.bin', 'rb') as fd:
#  data = fd.read()
#
#print(task05.repeating_key_xor(data, b'Terminator X: Bring the noise').decode())

#input = bytes()
#with open('6.bin', 'rb') as fd:
#  input = fd.read()
#results = find_keysize(input)
#results = sorted(results, key=task03.tuple_sort, reverse=True)
#result_keysizes = list()
#for item in results:
#  result_keysizes.append(item[1])
#pprint.pprint(results)
##print(result_keysizes)
#
