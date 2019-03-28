#!/usr/bin/env python3

# to get hamming function:
# in1 XOR in2, count differing bits with bitshifts to get hamming distance
#
# verification: hamming('this is a test', 'wokka wokka!!!') == 37

# key: b'Terminator X: Bring the noise' (not sticking the full output here)

import sys, task03 #, task05

def hamming_bits(in1, in2):
  if type(in1) == type(in2) == bytes:
    assert len(in1) == len(in2)
    in1 = int.from_bytes(in1, sys.byteorder)
    in2 = int.from_bytes(in1, sys.byteorder)
  assert type(in1) == type(in2) == int

  diff = in1 ^ in2
  out = 0
  while diff:
    out += diff & 1
    diff >>= 1
  return out

def find_keysize(input):
  assert type(input) == bytes
  assert len(input) >= 800

  normalized_results = list()
  for keysize in range(2, 40):
    result = 0
    for i in range(keysize):
      for j in range(20):
        result += hamming_bits(input[keysize*j + i], input[keysize*(j+1) + i])
    normalized_results.append(tuple([result / keysize, keysize]))
#  return normalized_results
  return task03.printsort(normalized_results)[0][1]


if __name__ == '__main__':
  import task02, base64

  with open('6.txt') as fd:
    rawdata = fd.read()
    rawdata = base64.b64decode(rawdata)

  keysize = find_keysize(rawdata)
  print(f'Estimated keysize: {keysize}')
  single_xor_chunks = list()
  for i in range(keysize):
    single_xor_chunks.append(bytes())
  for i in range(len(rawdata)):
    single_xor_chunks[i%keysize] += int.to_bytes(rawdata[i], 1, sys.byteorder)
  solved_chunks = list()
  for item in single_xor_chunks:
    solved_chunks.append(task03.dostuff(item))
  solved = bytes()
  for i in range(len(rawdata)):
    x, y = i % keysize, i // keysize
    solved += int.to_bytes(solved_chunks[x][y], 1, sys.byteorder)
  key = task02.xor_2_bytes(rawdata[:keysize], solved[:keysize])
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
