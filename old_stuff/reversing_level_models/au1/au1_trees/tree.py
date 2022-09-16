'''
header  x18 bytes
    u32 04                    04  04000000
    u32 file size       02 3C 20  203C0200
    u32 num                01 CF  CF010000
                           00 18  18000000
                           13 BD  BD130000
                           48 70  70480000

1   stride x28
    24B 6x float
    u32 int
    u32 float | int
    u32 ref to num
    u32 ref to num

2   size x1F3B0   stride x18   num x14D2
    12B 3x float
    12B float 0xC9 float

'''

from __future__ import annotations

from typing import BinaryIO
from dataclasses import dataclass
import struct


@dataclass(slots=True, frozen=True)
class Vec3f:
    x: float
    y: float
    z: float
    
    def xyoz(self) -> Vec3f:
        return Vec3f(self.x, self.y, -self.z)


class Header:
    def __init__(self, buf: bytes):
        self.magic,\
        self.file_size,\
        self.num,\
        self._1,\
        self._2,\
        self._3 = struct.unpack('4B5I', buf)


@dataclass(slots=True)
class Tree:
    pos: Vec3f
    height_maybe: Vec3f


class Something:
    def __init__(self, buf: bytes):
        self.v1 = struct.unpack('3f', buf[:12])
        self.v2 = struct.unpack('3f', buf[12:24])
        self.i1,\
        self.if1,\
        self.num1,\
        self.num2 = struct.unpack()


class TreeCol:
    def __init__(self, fo: BinaryIO):
        self.header(fo.read(24))
        self._
        

def main(path):
    with open(path, 'rb') as fo:
        tree = TreeCol(fo)


if __name__ == '__name__':
    import sys

    main(sys.argv[1])
