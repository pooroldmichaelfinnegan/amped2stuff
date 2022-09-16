from dataclasses import dataclass
import struct


class LineSize:
    def __init__(self, blob: bytes):
        self.line_length, = struct.unpack(f'I', blob[:4])
    def __call__(self):
        return self.line_length*12


class Line:
    def __init__(self, blob: bytes):
        self.length, = struct.unpack(f'I', blob[:4])
        self.line_bytes_size = struct.calcsize(f'{self.length*3}f')
        print(self.line_bytes_size)
        self.vertex_data = struct.unpack(f'{self.length*3}f', blob[4:4+self.line_bytes_size])
        self.points = Vec3Array(some_parser(self.vertex_data, 3, Vec3))


class Vec3Bytes:
    def __init__(self, blob: bytes):
        self.xyz = struct.unpack('3f', blob)
    def __call__(self):
        return Vec3(self.xyz)


class Vec3:
    def __init__(self, vector: list[float]):
        self.xyz = vector
        print(vector)
        self.x, self.y, self.z = self.xyz

        self.xyoz = [ self.x, self.y, -self.z ]


@dataclass
class Vec3Array:
    array: list[Vec3]

    def __post_init__(self):
        self.xyz = [ vec.xyz for vec in self.array ]
        self.xyoz = [ vec.xyoz for vec in self.array ]


def some_parser(lst: list | bytes, step: int, obj: bool = False) -> list:
    def slc(index):
        return slice( index*step, (index+1)*step )

    return [ obj(lst[slc(i)]) for i, _ in enumerate(lst[::step]) ]


class itr:
    def __init__(self, obj: bytes):
        self.obj = obj
    def __iter__(self):
        self.bites = self.obj
        self.lines = []
        return self
    def __next__(self):
        while self.bites:
            line_length = LineSize(self.bites)()
            print(line_length)
            self.lines += [ Line(self.bites).points.xyoz ]
            self.bites = self.bites[4+line_length:]
        return self.lines


with open('./NZ1.bnd', 'rb') as bnd:
    bnd = bnd.read()
    print(next(iter(itr(bnd))))
