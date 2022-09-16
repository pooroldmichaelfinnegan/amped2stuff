from typing import BinaryIO
import struct


class ChunkMeta:
    def __init__(self, file_binary, offset: int = 0):
        self.vertex_data_length, \
        self.index_data_length, \
        self._8, self._C, self._10, self._14, self._18, self._1C, self._20, self._24, \
        self.vertex_slice_count, \
        self.index_slice_count, \
        self._30, self._34, self._38, self._3C, \
        self._0100FF0F = struct.unpack('17I', file_binary[ offset : offset + 68 ])

        print(
            f'{self.vertex_data_length = }',
            f'{self.index_data_length = }',
            f'{self.vertex_slice_count = }',
            f'{self.index_slice_count = }',
            sep='\n'
        )

        self.vertex_meta_size = self.vertex_slice_count * 0xC
        self.index_meta_size = self.index_slice_count * 0xC


class Chunk:
    def __init__(self, file: bytes, offset: int = 0):
        self.file = file
        self.fileoff = file[offset:]

        self.meta = ChunkMeta(self.file, 3999812)
        self.vp = 0
        self.vmp = self.meta.vertex_data_length
        self.ip = self.meta.vertex_data_length + self.meta.vertex_meta_size
        self.imp = self.meta.vertex_data_length + self.meta.vertex_meta_size + self.meta.index_data_length
        print(
            f'{self.vmp = }',
            f'{self.ip = }',
            f'{self.imp = }',
            sep='\n'
        )

        self.vertex_raw_data = self.fileoff[:self.meta.vertex_data_length]
        self.index_raw_data = self.fileoff[ self.meta.vertex_data_length + self.meta.vertex_meta_size
                                      : self.meta.vertex_data_length + self.meta.vertex_meta_size + self.meta.index_data_length ]

        self.index_slices = self.slice_parser(self.imp, self.meta.index_meta_size, b'\x00\x00\x00\x00\x01\x00\x01\x00')
        self.vertex_slices = self.slice_parser(self.vmp, self.meta.vertex_meta_size, b'\x00\x00\x00\x00\x01\x00\x80\x00')

        self.index_data_raw_slices = self.data_raw_parser(self.index_raw_data, self.index_slices)
        self.vertex_data_raw_slices = self.data_raw_parser(self.vertex_raw_data, self.vertex_slices)


    def slice_parser(self, offset: int, length: int, splt: bytes) -> list:
        splted = self.fileoff[ offset+4 : offset+length-4 ].split(splt)
        lst = [ struct.unpack('I', i)[0] for i in splted ]
        print(lst)
        return [ slice(lst[i], lst[i+1]) for i, _ in enumerate(lst[:-1]) ] + [ slice(lst[-1], None) ]


    @staticmethod
    def junkdata2usefuldata(char: str, lst: list[bytes], stride: int = 0, size: int = 0, vertex: bool = 0):
        vertices = []
        type_size = struct.calcsize(char)
        if vertex:
            for block in lst:
                size = size if 0 < size < stride else stride
                indices = [ block[ index*stride : index*stride + size ] for index, _ in enumerate(block[::stride]) ]
                vertices = [ list(struct.unpack(char, i)) for i in indices ]
            return vertices
        return [ struct.unpack(char, j[i * type_size:(i + 1) * type_size])[0] for j in lst for i, _ in enumerate(j[::type_size]) ]


    @staticmethod
    def data_raw_parser(raw_data, slices: list[slice]) -> list:
        return [ raw_data[slce] for slce in slices ]


    @staticmethod
    def acc(bv: int, bo: int, c: int, ct: int, t: str, mx: list, mn: list):
        return {
            "bufferView": bv,
            "byteOffset": bo,
            "count": c,
            "componentType": ct,
            "type": t,
            "max": mx,
            "min": mn
        }


def calc_maxmin(*array_of_vec):
    _max = list(map(max, zip(*array_of_vec)))
    _min = list(map(min, zip(*array_of_vec)))
    return _max, _min


if __name__ == '__main__':
    with open('./bk1/BK1.pgf', 'rb') as pgf_buffer:
        pgf = pgf_buffer.read()

    ## NZ1.pgf
    # chunk_meta = ChunkMeta(pgf, 3952332)
    # chunk = Chunk(pgf, 3952400)

    ## LX1.pgf
    chunk_meta = ChunkMeta(pgf, 3999812)
    chunk = Chunk(pgf, 3999880)

    # print(len(chunk.vertex_data_raw_slices[0:1]))
    # print(chunk.junkdata2usefuldata('H', chunk.index_data_raw_slices[0:1]))
    # print(chunk.junkdata2usefuldata('3f', chunk.vertex_data_raw_slices[:31], sparse=28, offset=0, vertex=True))

    for i in range(66):
        I = chunk.junkdata2usefuldata('H', chunk.index_data_raw_slices[i:i+1])
        MAX, MIN = max(I), min(I)

        count = len(I)
        # print(chunk.acc(0, chunk.index_slices[i].start, count, 5123, 'SCALAR', [ MAX ], [ MIN ]))

        I = chunk.junkdata2usefuldata('3f', chunk.vertex_data_raw_slices[i:i+1], stride=28, size=12, vertex=1)
        MAX, MIN = max(I), min(I)

        count = len(I)
        print(chunk.acc(0, chunk.vertex_slices[i].start, count, 5126, 'VEC3', MAX, MIN ))
