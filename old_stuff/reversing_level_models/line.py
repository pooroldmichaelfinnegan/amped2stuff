from __future__ import annotations

from typing import BinaryIO, NamedTuple, Self
import struct


class Lines(list):
    def oz(self) -> 'Lines':
        lines = Lines()
        for line in self:
            start = line.start.xyoz()
            end = line.end.xyoz()
            lines += [Line(start, end)]
        return lines
    @staticmethod
    def from_line_loop(array: list) -> 'Lines':
        array = array + [array[0]]
        return Lines(Line(array[i], array[i+1]) for i, _ in enumerate(array[:-1]))
    @staticmethod
    def from_linearray(array: list) -> 'Lines':
        return Lines(Line(array[i], array[i+1]) for i, _ in enumerate(array[:-1]))


class Line(NamedTuple):
    start: Vec
    end: Vec


class Vec(NamedTuple):
    x: float
    y: float
    z: float

    def xyoz(self) -> 'Vec':
        return Vec(self.x, self.y, -self.z)
    def toOBJ(self, obj: OBJ) -> tuple[int, str]:
        return obj.nv, 'v {self.x} {self.y} {self.z}'


class OBJ:
    def __init__(self):
        self.v: str = ''
        self.nv: int = -1


def bytes2array(bites: bytes) -> list:
    print(f'{len(bites) = }')
    print(f'{len(bites)/12 = }')
    return [Vec(*struct.unpack('3f', bites[i*12:i*12+12])) for i, _ in enumerate(bites[::12])]


def main(path: str):
    print('main')
    with open(path, 'rb') as fo:
        size = int.from_bytes(fo.read(4), 'little')
        la = bytes2array(fo.read(size*12))
        finish = Lines.from_line_loop(la)
        size = int.from_bytes(fo.read(4), 'little')
        la = bytes2array(fo.read(size*12))
        inner = Lines.from_line_loop(la)
        size = int.from_bytes(fo.read(4), 'little')
        la = bytes2array(fo.read(size*12))
        outer = Lines.from_line_loop(la)
        size = int.from_bytes(fo.read(4), 'little')
        la = bytes2array(fo.read(size*24))
        reset = Lines.from_linearray(la)

    print(reset.oz())


if __name__ == '__main__':
    import sys

    main(sys.argv[1])
