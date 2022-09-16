from __future__ import annotations

from dataclasses import dataclass
from typing import NamedTuple
import struct


def cls_from_bytes(cls, buffer: bytes, _fmt: str) -> object:
    assert( len(buffer) == struct.calcsize(_fmt), f' buffer ({len(buffer)}) size doenst match struct format size ({struct.calcsize(_fmt)}) ')
    return cls( *struct.unpack(_fmt, buffer) )


def array_parser(blob: bytes, array_type: list | tuple = list, data_type: type = int, array_size: int = 1) -> list | tuple:
    ## TODO
    pass


def split_bytes(buffer: bytes, stride: int, length: int = 0, offset: int = 0) -> list:
    ''' split_bytes(b'\x01\x00\x02\x00', 2) -> [ b'\x01\x00', b'\x02\x00' ] 
        split_bytes(b'\x01\x00\x00\x00\x02\x00\x00\x00', 4, 1) -> [ b'\x01', b'\x02' ] '''
    length = length if 0 < length < stride else stride
    return [ buffer[ offset + index*stride : offset + index*stride + length ] for index, _ in enumerate(buffer[::stride]) ]


def split_bytes_sections(buffer: bytes, stride: int, length: int) -> list[bytes]:
    assert not stride % length, 'split_bytes_sections'

    ratio = stride // length
    l: list[bytes] = [b'' for _ in range(ratio)]
    
    for index, byte in enumerate(buffer):
        l[index] += byte
        
    return l


class ColorRGBA(NamedTuple):
    r: int; g: int; b: int; a: int

    @classmethod
    def from_bytes(cls, buffer: bytes):
        ''' assuming 8bit colors '''
        return cls(*struct.unpack('4B', buffer))
    def to_bytes(self) -> bytes:
        ''' assuming 8bit colors '''
        return struct.pack('4B', self.r, self.g, self.b, self.a)


def round( *attrs, coef: int = 2 ) -> list:
    return [ attr - attr%coef for attr in attrs ]
