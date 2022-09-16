from __future__ import annotations

from typing import (
        BinaryIO,
        Literal
    )
from io import BytesIO
from dataclasses import dataclass

from xpr0 import (
        ColorRGB,
        ColorRGBA
    )


# https://en.wikipedia.org/wiki/S3_Texture_Compression#DXT1

class DXT2or3:
    def __init__(self, buffer: bytes):
        assert len(buffer) == 16, 'DXT2or3'

        bio = BytesIO(buffer)

        bio.read(8)
        self.dxt1 = DXT1(bio.read(8))


class DXT1:
    def __init__(self, buffer: bytes):
        assert len(buffer) == 8, 'DXT1'

        bio = BytesIO(buffer)

        self.color_0_bytes: bytes = ColorRGB565(bio.read(2))
        self.color_1_bytes: bytes = ColorRGB565(bio.read(2))
        self.lookup_table: bytes = LookupTable(bio.read(4))

        self.color_0_int: int = int.from_bytes(self.color_0_bytes)
        self.color_1_int: int = int.from_bytes(self.color_1_bytes)

        if self.color_0_int > self.color_1_int:
            self.color_2_int = self.color_0_int*2/3 + self.color_0_int*1/3
            self.color_3_int = self.color_0_int*1/3 + self.color_0_int*2/3


class LookupTable:
    def __init__(self, buffer: bytes):
        assert len(buffer) == 4, 'LookupTable'

        


# dataclass(slots=True)
class ColorRGB565(bytes):
    # rgb565: bytes

    def toRGB(self, endian: Literal['little', 'big'] = 'big') -> tuple[int]:
        assert len(self) == 2, 'ColorRGB565'

        binary = bin(int.from_bytes(self, endian))[2:].zfill(16)
        r: int = int(binary[slice( 0,  5)], 2)
        g: int = int(binary[slice( 5, 11)], 2)
        b: int = int(binary[slice(11, 16)], 2)

        return r, g, b
    
    def toColorRGB(self) -> ColorRGB:
        return ColorRGB(self.toRGB())


