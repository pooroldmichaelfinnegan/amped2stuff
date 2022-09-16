from __future__ import annotations

from typing import (
    Any,
    BinaryIO,
    Sequence
)
from dataclasses import dataclass
import io
import struct


@dataclass(slots=True)
class Vec3:
    x: float
    y: float
    z: float
    def __repr__(self):
        return f'{f"{self.x}":20}{f"{self.y}":20}{f"{self.z}":20}'
    def up(self):
        return [ self.x, self.y, self.z ]
    def opposite_z(self) -> 'Vec3':
        return Vec3(self.x, self.y, -self.z)
    def to_bytes(self) -> bytes:
        return b''.join([ struct.pack( '3f', *[ float(v) for v in self._asdict().values() ])])
    @classmethod
    def from_bytes(cls, buffer: bytes):
        return cls(*struct.unpack('3f', buffer))


def split_0x0100FF0F(fo: BinaryIO, BufferIO: bool = False) -> list[BinaryIO | bytes]:
    splitted = fo.read().split(b'\x01\x00\xFF\x0F')
    if BufferIO:
        for i in splitted:
            yield io.BytesIO(i)
    else:
        for i in splitted:
            yield i


def calc_maxmin(array: Sequence[Any]) -> list[Any, Any]:
    Max = list(map(max, zip(*array)))
    Min = list(map(min, zip(*array)))
    return Max, Min
