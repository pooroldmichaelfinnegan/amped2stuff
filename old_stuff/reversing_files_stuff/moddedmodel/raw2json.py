class ChunkMeta:
    length = 64

    def __init__(self, file: bytes, offset: int = 0):
        import struct

        self.vertex_data_length, \
        self.index_data_length, \
        self._8, \
        self._C, \
        self._10, \
        self._14, \
        self._18, \
        self._1C, \
        self._20, \
        self._24, \
        self.vertex_slice_count, \
        self.index_slice_count, \
        self._30, \
        self._34, \
        self._38, \
        self._3C = struct.unpack('16I', file[ offset : offset+64 ])

        self.vertex_meta_size = self.vertex_slice_count * 0xC
        self.index_meta_size = self.index_slice_count * 0xC


def calc_maxmin(*array_of_vec):
    _max = list(map(max, zip(*array_of_vec)))
    _min = list(map(min, zip(*array_of_vec)))
    return _max, _min


class Chunk:
    def __init__(self, file: bytes, offset: int = 0):
        self.file = file
        self.fileoff = file[offset:]

        self.meta = ChunkMeta(self.file, 3952332)
        self.vp = 0
        self.vmp = self.meta.vertex_data_length
        self.ip = self.meta.vertex_data_length + self.meta.vertex_meta_size
        self.imp = self.meta.vertex_data_length + self.meta.vertex_meta_size + self.meta.index_data_length

        self.vertex_raw_data = self.fileoff[:self.meta.vertex_data_length]
        self.index_raw_data = self.fileoff[ self.meta.vertex_data_length + self.meta.vertex_meta_size
                                      : self.meta.vertex_data_length + self.meta.vertex_meta_size + self.meta.index_data_length ]

        self.index_slices = self.slice_parser(self.imp, self.meta.index_meta_size, b'\x00\x00\x00\x00\x01\x00\x01\x00')
        self.vertex_slices = self.slice_parser(self.vmp, self.meta.vertex_meta_size, b'\x00\x00\x00\x00\x01\x00\x80\x00')

        self.index_data_raw_slices = self.data_raw_parser(self.index_raw_data, self.index_slices)
        self.vertex_data_raw_slices = self.data_raw_parser(self.vertex_raw_data, self.vertex_slices)


    def slice_parser(self, offset: int, length: int, splt: bytes) -> list:
        import struct

        splted = self.fileoff[offset+4:offset+length-4].split(splt)
        lst = [ struct.unpack('I', i)[0] for i in splted ]
        return [ slice(lst[i], lst[i+1]) for i, _ in enumerate(lst[:-1]) ] + [ slice(lst[-1], None) ]


    @staticmethod
    def unpack_blocks_of_vertex_data(blocks: list[list[bytes]], sparse: int = 12, offset: int = 0) -> list[float, float, float]:
        import struct
        
        fmt = '3f'
        fmt_size = struct.calcsize(fmt)
        vertices = []

        for block in blocks:
            # items = [ block[item*sparse:(item+1)*sparse] for item, _ in enumerate(block[::sparse]) ]
            items = idk_parser(block, sparse)

            vertices += [ list(struct.unpack(fmt, i[:fmt_size])) for i in items ]

        return vertices

    @staticmethod
    def unpack_blocks_of_index_data(indices: list[list[int]], fmt: str = 'I') -> list[int]:
        import struct

        fmt_size = struct.calcsize(fmt)
        strips = []

        # for block in indices:
        #     strips += idk_parser_unpacker(block, fmt_size, fmt=fmt)
        strips = [ struct.unpack(fmt, block[index * fmt_size:(index + 1) * fmt_size])[0] for block in indices for index, _ in enumerate(block[::fmt_size]) ]

        tris = [ strips[:3] ]
        tris += [[ strips[i-1], strips[i-2], strips[i] ] for i in range(3, len(strips[3:])) ]

        tris_2 = strips[:3]
        for i in range(3, len(strips[3:])):
            if i % 2:
                tris_2 += [ strips[i-1], strips[i-2], strips[i] ]
            else:
                tris_2 += [ strips[i-2], strips[i-1], strips[i] ]

        tris_up = [ i for j in tris for i in j ]
        # tris2_up = [ i for j in tris_2 for i in j ] 

        return tris_2


    @staticmethod
    def data_raw_parser(raw_data, slices: list[slice]) -> list:
        return [ raw_data[slce] for slce in slices ]


def idk_parser(lst: list, step: int) -> list:
    def slc(index):
        return slice( index*step, (index+1)*step )

    return [ lst[slc(i)] for i, _ in enumerate(lst[::step]) ]


def idk_parser_unpacker(lst: list, step: int, fmt: str = 'I') -> list:
    import struct

    def slc(index):
        return slice( index*step, (index+1)*step )

    return [ struct.unpack(fmt, lst[slc(i)]) for i, _ in enumerate(lst[::step]) ]


if __name__ == '__main__':
    with open('./NZ1.pgf', 'rb') as pgf_buffer:
        pgf = pgf_buffer.read()

    chunk_meta = ChunkMeta(pgf, 3952332)
    chunk = Chunk(pgf, 3952400)

    indices, vertices = [], []

    for i in range(31):
        indices += [ chunk.unpack_blocks_of_index_data(chunk.index_data_raw_slices[i:i+1], fmt='H') ]
        vertices += [ chunk.unpack_blocks_of_vertex_data(chunk.vertex_data_raw_slices[i:i+1], sparse=28) ]
    
    jsn = { 'indices': indices, 'vertices': vertices }

    import json

    with open('./model_tris.json', 'wt') as JSON:
        json.dump(jsn, JSON)
