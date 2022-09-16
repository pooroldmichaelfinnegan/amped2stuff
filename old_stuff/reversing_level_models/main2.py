from __future__ import annotations


# from typing_extensions import (
#     Self
# )
from typing import (
        Any,
        BinaryIO,
        Literal,
        NamedTuple,
        overload
    )
from dataclasses import dataclass
import io, re, struct

# local
from tools import (
    Vec3,
    split_0x0100FF0F,
    calc_maxmin
)


class PGF:
    def __init__(self, fo: BinaryIO, **kwargs):
        self._pgf_gen = split_0x0100FF0F(fo, BufferIO=True)

        self.magic = struct.unpack('4s', next(self._pgf_gen).read())
        self.pgf_header = PGFHeader(next(self._pgf_gen))
        next(self._pgf_gen)  # xpr0 data
        next(self._pgf_gen)  # 

        next(self._pgf_gen)  # random 0x0100FF0F in AU1.pgf
        self.model_header = ModelHeader(next(self._pgf_gen))
        self.model_buffers = ModelBuffers(next(self._pgf_gen), self.model_header)
        self.model = Model(self.model_buffers, **kwargs)


class PGFHeader:
    def __init__(self, fo: BinaryIO):
        self.file_size, \
        _, \
        self.xpr_data_size, \
        self.xpr_slice_count, \
        _, \
            = struct.unpack('5I', fo.read())


class ModelHeader:
    def __init__(self, fo: BinaryIO):
        b = fo.read()
        self.vertex_data_length, \
        self.index_data_length, \
        _, _, _, _, _, _, _, _, \
        self.vertex_slice_count, \
        self.index_slice_count, \
        _, _, _, _, \
            = struct.unpack('16I', b)


class ModelBuffers:
    def __init__(self, fo: BinaryIO, model_header: ModelHeader):
        self.model_header = model_header

        ## vertices
        self.vertex_buffer = fo.read(model_header.vertex_data_length)

        ## vertex slices
        vertex_slice_buffer_size = model_header.vertex_slice_count * slice_vertex.size
        self.vertex_slices_buffer = fo.read(vertex_slice_buffer_size)

        ## indices
        self.index_buffer = fo.read(model_header.index_data_length)

        ## index slices
        index_slice_buffer_size = model_header.index_slice_count * slice_index.size
        self.index_slices_buffer = fo.read(index_slice_buffer_size)


class Model:
    def __init__(self, model_buffers: ModelBuffers, global_slice, **kwargs):
        # self.model_buffers = model_buffers

        # vertex slices
        self.vertex_slices = PGFSlice().list_of_slices( buffer    = model_buffers.vertex_slices_buffer,
                                                        slc       = slice_vertex,
                                                        slice_end = model_buffers.model_header.vertex_data_length
                                                      )

        # index slices
        self.index_slices = PGFSlice().list_of_slices( buffer    = model_buffers.index_slices_buffer,
                                                       slc       = slice_index,
                                                       slice_end = model_buffers.model_header.index_data_length
                                                     )

        assert len(self.index_slices) == len(self.vertex_slices)
        self.aus1_section_strides = [28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 24, 24, 24, 28, 28, 28, 28, 24, 24, 28, 24, 24, 28, 28, 24, 28, 24, 24, 28, 24, 24, 28, 24, 24, 28, 24, 24, 24, 28, 24, 24, 28, 24, 24, 28, 24, 24, 28, 24, 28, 28, 24, 24, 28, 24, 28, 24, 24, 28, 28, 24, 24, 28, 24, 28, 28, 24, 28, 28, 24, 28, 28, 28, 24, 24, 28, 28, 24, 28, 28, 28, 28, 28, 24, 24, 24, 28, 24, 28, 24, 24, 28, 24, 24, 32, 24, 32, 24, 32, 24, 32, 24, 32, 24, 28, 24, 24, 28, 24, 24, 28, 28, 28, 28, 28, 28, 28, 28, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 24, 28, 28, 28, 32, 24, 24, 32, 24, 24, 32, 24, 24, 32, 24, 24, 32, 24, 24, 32, 24, 24, 32, 24, 24, 32, 24, 24, 32, 24, 24, 32, 24, 24, 32, 24, 24, 32, 24, 24, 32, 24, 24, 32, 24, 24, 32, 24, 24, 32, 24, 24, 32, 24, 24, 32, 24, 24, 32, 24, 24, 32, 24, 24, 32, 24, 24, 28, 24, 24, 24, 28, 32, 32, 32, 32, 32, 32, 24, 24, 24, 32, 32, 32, 32, 32, 24, 24, 24, 28, 28, 32, 28, 28, 32, 32, 32, 32, 32, 24, 24, 24, 24, 24, 24, 24, 24, 24, 28, 32, 32, 32, 24, 28, 28, 24, 24, 28, 28, 28, 28, 28, 28, 24, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 32, 28, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 28, 24, 24, 24, 24, 24, 24, 24, 32, 32, 32, 28, 28, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 32, 32, 32, 32, 32, 32, 28, 28, 28, 28, 28, 24, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 28, 28, 28, 28, 28, 32, 32, 32, 32, 32, 32, 32, 32, 28, 28, 32, 32, 28, 28, 28, 28, 28, 28, 28, 32, 32, 28, 32, 28, 32, 32, 32, 32, 24, 28, 32, 32, 32, 16, 16, 16, 16]
        self.aus1_section_strides2 = [28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 24, 24, 24, 28, 28, 28, 28, 24, 24, 28, 24, 24, 28, 28, 24, 28, 24, 24, 28, 24, 24, 28, 24, 24, 28, 24, 24, 24, 28, 24, 24, 28, 24, 24, 28, 24, 24, 28, 24, 28, 28, 24, 24, 28, 24, 28, 24, 24, 28, 28, 24, 24, 28, 24, 28, 28, 24, 28, 28, 24, 28, 28, 28, 24, 24, 28, 28, 24, 28, 28, 28, 28, 28, 24, 24, 24, 28, 24, 28, 24, 24, 28, 24, 24, 32, 24, 32, 24, 32, 24, 32, 24, 32, 24, 28, 24, 24, 28, 24, 24, 28, 28, 28, 28, 28, 28, 28, 28, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 24, 28, 28, 28, 32, 24, 24, 32, 24, 24, 32, 24, 24, 32, 24, 24, 32, 24, 24, 32, 24, 24, 32, 24, 24, 32, 24, 24, 32, 24, 24, 32, 24, 24, 32, 24, 24, 32, 24, 24, 32, 24, 24, 32, 24, 24, 32, 24, 24, 32, 24, 24, 32, 24, 24, 32, 24, 24, 32, 24, 24, 32, 24, 24, 32, 24, 24, 28, 24, 24, 24, 28, 32, 32, 32, 32, 32, 32, 24, 24, 24, 32, 32, 32, 32, 32, 24, 24, 24, 28, 28, 32, 28, 28, 32, 32, 32, 32, 32, 24, 24, 24, 24, 24, 24, 24, 24, 24, 28, 32, 32, 32, 24, 28, 28, 24, 24, 28, 28, 28, 28, 28, 28, 24, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 32, 28, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 28, 24, 24, 24, 24, 24, 24, 24, 32, 32, 32, 28, 28, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 28, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 32, 32, 32, 32, 32, 32, 28, 28, 28, 28, 28, 24, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 28, 28, 28, 28, 28, 32, 32, 32, 32, 32, 32, 32, 32, 28, 28, 32, 32, 28, 28, 28, 28, 28, 28, 28, 32, 32, 28, 32, 28, 32, 32, 32, 32, 24, 28, 32, 32, 32, 16, 16, 16, 16]
        self.NZ1_model_vertex_stride_mapping = [28]*31 + [24]*2 + [28]*8 + [32]*7 + [24]*31 + [32]*12 + [20]*12 + [28]*1
        self.slices = [slice(31), slice(31, 33), slice(33, 41), slice(41, 48), slice(48, 60), slice(60, 77), slice(77, 78), slice(78, 79), slice(79, 80), slice(80, 91), slice(91, 103), slice(103, 104)]
        self.model_sections = [ ModelSection( model_buffers.index_buffer[islice], 
                                              model_buffers.vertex_buffer[vslice],
                                              stride,
                                              islice,
                                              vslice
                                            ) for islice, vslice, stride in zip( self.index_slices[global_slice],
                                                                                 self.vertex_slices[global_slice],
                                                                                 #self.NZ1_model_vertex_stride_mapping
                                                                                 self.aus1_section_strides2
                                                                               )
                              ]

    def to_floats(self, slc: slice = slice(None)):
        vs = ''
        for i in self.model_sections:
            vs += '\n' + i.vertices.to_string()
        return vs, ''

    def to_bytes(self, slc: slice = slice(None)):
        vb, ib = b'', b''
        nv, ni = 0, 0

        for i in self.model_sections[slc]:
            vb += i.vertices.opposite_z().to_bytes()
            newi = [ i+nv for i in i.indices.triStrips2tri() ]
            ib += b''.join(struct.pack('I', j) for j in newi)
            nv += len(i.vertices)

        return vb, ib

    def toOBJ(self, slc: slice = slice(None)):
        v: str = ''
        i: str = ''
        vn: int = 0  # vertex count to offset indices
        for ms in self.model_sections[slc]:
            msi = ms.indices
            for V in ms.vertices:
                v += f'\nv {V.x} {V.y} {-V.z}'
            i += '\n'
            # i += '\n'.join(f'f {I[0]+vn} {I[1]+vn} {I[2]+vn}' for I in split_sequence(ms.indices.triStrips2tri(), 3))
            tris = split_sequence(ms.indices, 3)
            i += '\n'.join(f'f {I[0]+vn+1} {I[1]+vn+1} {I[2]+vn+1}' for I in tris)
            vn += len(ms.vertices)

        return v, i

        # def alternate(i, xs):
        #     even = i % 2 == 0
        #     return xs if even else (xs[0], xs[2], xs[1])
        # tris = np.array([
        #     alternate(i, (indices[i], indices[i + 1], indices[i + 2]))
        #     for i in range(0, len(indices) - 2)
        # ])


class ModelSection:
    def __init__(self, index_section: bytes, vertex_section: bytes, stride: int, islice: slice, vslice: slice, offset: int = 0):
        self.index_section = index_section
        self.vertex_section = vertex_section
        self.stride = stride
        self.islice, self.vslice = islice, vslice

        self.num_of_indices = len(self.index_section) // 2  # 2 is bytesize (uint16)
        self.indices = iarray( struct.unpack( f'{self.num_of_indices}H', self.index_section ))
        print(f'{len(self.indices)=}')

        self.splt = split_sequence(self.vertex_section, stride)

        # self.vertices = varray([Vec3( *struct.unpack_from('12x', i)) for i in self.splt]) # split_sequence(self.vertex_section, stride)])
        self.vertices = varray([Vec3( *struct.unpack_from('12x', i)) for i in self.splt]) # split_sequence(self.vertex_section, stride)])


    def toOBJ(self):
        v: str = ''
        indices: str = ''
        vn: int = 0
        for V in self.vertices:
            v += f'\nv {V.x} {V.y} {-V.z}'
            # i += '\n'.join(f'f {I[0]+vn} {I[1]+vn} {I[2]+vn}' for I in split_sequence(ms.indices.triStrips2tri(), 3))
        tris = split_sequence(self.indices.triStrips2tri(), 3)
            # print(f'{len(tris)}')
        indices += '\n'.join(f'\nf {I[0]+vn+1} {I[1]+vn+1} {I[2]+vn+1}' for I in tris)
        vn += len(self.vertices)
        print(f'{len(indices)=}')
        return v, indices

    def get_slices(self) -> tuple[slice, slice]:
        return (self.islice, self.vslice)


class iarray(list):
    def triStrips2tri(self, blend_alg: bool = False):
        if not blend_alg:
            temp = self[:3]
            for i in range(3, len(self[3:])):
                if i % 2: temp += [ self[i-1], self[i-2], self[i] ]
                else: temp += [ self[i-2], self[i-1], self[i] ]
            return iarray(temp)
        else:
            def alternate(i, xs):
                even = i % 2 == 0
                return xs if even else (xs[0], xs[2], xs[1])
            tris = [
                alternate(i, (self[i], self[i + 1], self[i + 2]))
                for i in range(0, len(self) - 2)
            ]
    # fmt: Literal['B', 'H', 'I']
    def to_bytes(self, fmt: str) -> bytes:
        return b''.join( struct.pack(fmt, index) for index in self )
    def gltf_data(self) -> dict[str, Any]:
        return {
            'byte_length': len(self),
            'max': max(self),
            'min': min(self)
        }


class varray(list):
    def tolst(self):
        l = []
        for v in self:
            l += v.up()
        return l
    def to_string(self):
        return '\n'.join(repr(vec) for vec in self)
    def opposite_z(self) -> 'varray':
        return varray([ vec3.opposite_z() for vec3 in self ])
    def to_bytes(self) -> bytes:
        return b''.join( vec3.to_bytes() for vec3 in self )
    def gltf_data(self) -> dict[str, Any]:
        Max, Min = calc_maxmin(self)
        return {
            'byte_length': len(self),
            'max': Max,
            'min': Min
        }


class SliceType(NamedTuple):
    signature: bytes  # re 'lookahead' expression
    size: int
    fmt: str  # should move
slice_xpr = SliceType(b'\x01\x00\x04\x00', 20, '4s4I')
slice_index = SliceType(b'(?=\x01\x00\x01\x00)', 12, '4s2I')
slice_vertex = SliceType(b'(?=\x01\x00\x80\x00)', 12, '4s2I')


class PGFSlice(list):
    def list_of_slices(self, buffer, **kwargs) -> list[slice]:
        splited = self.split_buffer(buffer, **kwargs)
        unpacked = self.unpack_bytes(splited[1:], **kwargs)
        return self.to_slices(unpacked, **kwargs)
    @staticmethod
    def split_buffer(buffer: bytes, slc: SliceType, **kwargs) -> list[bytes]:
        return re.split(slc.signature, buffer)
    @staticmethod
    def unpack_bytes(lst: list[bytes], slc: SliceType, **kwargs) -> list[Any]:
        return [ struct.unpack_from(slc.fmt, i)[1] for i in lst ]
    @staticmethod
    def to_slices(lst: list[int], slice_end: int | None = None, **kwargs) -> list[slice]:
        if slice_end is not None:
            lst += [ slice_end ]
        return [ slice(lst[i], lst[i + 1]) for i, _ in enumerate(lst[:-1]) ]


def split_sequence(sequence: Any, stride: int = 1, offset: int = 0, size: int = 0) -> list[Any]:
    size = size if 0 < size < stride else stride
    return [ sequence[offset + i*stride:offset + i*stride + size] for i, _ in enumerate(sequence[::stride])]


pgf: PGF
def main(path):
    global pgf
    import time
    pc = time.perf_counter()

    with io.open(path, 'rb') as fo:
        pgf = PGF(fo, global_slice=slice(41))
    for index, value in enumerate(pgf.model.model_sections):
        islc, vslc = value.get_slices()
        # print('slcs += value.get_slices()              ', time.perf_counter() - pc);  pc = time.perf_counter()
        vertices, indices = value.toOBJ()
        print(f'{len(vertices) = }\n{len(indices) = }\n')
        # print('vertices, indices = pgf.model.toOBJ()   ', time.perf_counter() - pc);  pc = time.perf_counter()
        # section_list += [vertices + indices]
        # print('section_list += [vertices + indices]   ', time.perf_counter() - pc);  pc = time.perf_counter()
        # print('index', index)

    # for index, value in enumerate(section_list):
    #     islc, vslc = slcs[index]
        with open(f'./au1/model_normals/{index}__i{islc.start}_{islc.stop}__v{vslc.start}_{vslc.stop}.obj', 'wt') as f:
            f.write(vertices + indices)
            print(index, 'good')


if __name__ == '__main__':
    # import sys
    #   
    # if sys.argv[1]:
    #     main(sys.argv[1])
    # else:
    main('./au1/AU1.pgf')
