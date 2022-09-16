from __future__ import annotations

from typing import (
    BinaryIO
)
import io
import struct
from typing_extensions import Self

from tools import (
    Vec3,
    ColorRGBA
)


## direct3d fvf's (flexible vertex formats)

class _28:
    def __init__(self, pos: Vec3, color: ColorRGBA, normal: Vec3):
        self.position = pos
        self.diffuse_color = color
        self.normal = normal

    @classmethod
    def from_bytes(buffer: bytes) -> _28:
        assert len(buffer) == 28, 'len _28 vertex format'
        
        bufio = io.BytesIO(buffer)
        
        pos = struct.unpack('3f', bufio.read(12))
        color = bufio.read(4)
        normal = struct.unpack('3f', bufio.read(12))
        return _28(
            Vec3(pos),
            ColorRGBA.from_bytes(color),
            Vec3(normal)
        )

class _24: ...

class _32: ...