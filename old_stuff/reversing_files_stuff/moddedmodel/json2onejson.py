import json
import struct


with open('./model_tris.json') as iv:
    JSON = json.load(iv)


index_lens = [ len(i) for i in JSON['vertices'] ]
index_lens_off = [ 0 ] + index_lens
new_bytes = b''

for i, l in enumerate(JSON['indices']):
    new_bytes += b''.join(struct.pack('I', j + sum(index_lens_off[:i+1])) for j in l)

vb = b''
for vec in JSON['vertices']:
    for x, y, z in vec:
        vb += b''.join(struct.pack('f', i) for i in [x, y, -z])

# print(vb)

with open('./model_tris.bin', 'wb') as BIN:
    BIN.write(new_bytes + vb)

# I = JSON['indices'][0]
# print(len(I))
# obj = ''.join( f'f { I[(i*3)]+1 } { I[(i*3)+2]+1 } { I[(i*3)+1]+1 }\n' for i, _ in enumerate(I[::3]) )

# print(obj)
