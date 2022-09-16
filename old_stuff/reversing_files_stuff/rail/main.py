from dataclasses import dataclass, field
import struct


class RL:
    def __init__(self, blob: bytes):
        self.head = Head(blob[:12])
        self.headless = blob[12:]

        self._meta_sparse = 36
        self.metas = Metas(self.headless[ : self.head.meta_size * self._meta_sparse ])

        self.vertex_data_offset = self.head.meta_size * self._meta_sparse
        self.vertex_data_offset_inc_head = self.vertex_data_offset + 12
        self.vertex_data = self.headless[ self.vertex_data_offset : ]

    def to_gltf(self):
        self.glTF = gltf()

        self.glTF.add_bv(self.glTF.bvs, 0, self.head.file_size - self.vertex_data_offset + 12, self.vertex_data_offset_inc_head, 34962)
        self.glTF.mshs += [{ 'primitives': [{}]}]

        for meta in self.metas.meta_list:
            raw = self.headless[ meta.offset_to_vertices : meta.offset_to_vertices + meta.vertex_count * 12 ]
            self.rail = Rail(raw)

            mx, mn = calc_maxmin(*self.rail.vertices)

            self.glTF.add_acc(self.glTF.accs, 0, meta.offset_to_vertices, meta.vertex_count, 5126, 'VEC3', mx, mn )
            self.glTF.add_att(self.glTF.mshs[0]['primitives'], len(self.glTF.accs)-1, 3)
        
        print(
            f'{self.glTF.mshs}',
            f'{self.glTF.accs}',
            f'{self.glTF.bvs}'
        )


class Head:
    def __init__(self, blob: bytes):
        self.unknown_uint32, \
        self.meta_size, \
        self.file_size = struct.unpack('3I', blob)


class Metas:
    def __init__(self, blob: bytes):
        self.sparse = 36

        self.meta_list = [ Meta(blob[ index * self.sparse : (index+1) * self.sparse ]) for index, _ in enumerate(blob[::self.sparse]) ]


class Meta:
    def __init__(self, blob):
        self.type_maybe = blob[:4]
        self.four_unknown_floats = struct.unpack('4f', blob[4:20])
        self.vertex_count, \
        self.offset_to_vertices, \
        self.offset_to_first_half_of_unknown_unit_vectors, \
        self.offset_to_second_half_of_unknown_unit_vectors = struct.unpack('4I', blob[20:36])


class Rail:
    def __init__(self, raw: bytes):
        self.raw = raw

        self.vertices = [ Vec3(raw[i*12:(i+1)*12]).vec3 for i, _ in enumerate(raw[::12]) ]
    


class Vec3:
    def __init__(self, data: bytes):
        if len(data) != 12: raise 'vec not 12 bytes'

        self.x, self.y, self.z = struct.unpack('3f', data)

        self.vec3 =[ self.x, self.y, self.z ]
        self.vec3oz = [ self.x, self.y, -self.z ]


def calc_maxmin(*array_of_vec):
    _max = list(map(max, zip(*array_of_vec)))
    _min = list(map(min, zip(*array_of_vec)))
    return _max, _min


@dataclass
class gltf:
    nds: list = field(default_factory=list)
    mshs: list = field(default_factory=list)
    accs: list = field(default_factory=list)
    bvs: list = field(default_factory=list)

    @staticmethod
    def add_msh(mshs, p, m):
        mshs += [{
            'primitives': [{
                'attributes': {
                    'POSITION': p
                },
                'mode': m
            }]
        }]

    @staticmethod
    def add_att(prms, p, m):
        prms += [{
                'attributes': {
                    'POSITION': p
                },
                'mode': m
            }]

    @staticmethod
    def add_acc(accs, bv, bo, c, cp, t, mx, mn):
        accs += [{
            'bufferView': bv,
            'byteOffset': bo,
            'count': c,
            'componentType': cp,
            'type': t,
            'max': mx,
            'min': mn
        }]

    @staticmethod
    def add_bv(bvs, b, bl, bo, t):
        bvs += [{
            'buffer': b,
            'byteLength': bl,
            'byteOffset': bo,
            'target': t,
        }]

    def out(self):
        print(
            f'{self.nds}',
            f'{self.mshs}',
            f'{self.accs}',
            f'{self.bvs}',
            sep='\n\n'
        )


if __name__ == '__main__':
    with open('./NZ1.rl.bin', 'rb') as rl:
        rl = rl.read()

        r = RL(rl)

        r.to_gltf()
