from __future__ import annotations

from dataclasses import dataclass
from re import T
from typing import (
    BinaryIO,
    Literal
)
import io
import struct
import numpy as np

### local imports
from tools import (
        ColorRGBA,
        split_bytes,
        split_bytes_sections,
        round
    )
from bmp import (
        BMPFile,
        BMPHeader,
        DIBHeader,
        BMPColorTable,
        BMPPixelArray
    )


class XPR0:
    def __init__( self, buffer: BinaryIO ):
        ### HEAD ###
        self.magic, \
        self.file_size, \
        self.head_size = struct.unpack('4s2I', buffer.read(12))

        self.meta = Meta04(buffer.read(self.head_size - 12))

        ### COLOR ARRAY
        self.color_array = ColorArray.from_bytes(buffer.read())


class Meta04:
    ''' 01 00 04 00 '''
    def __init__(self, buffer: bytes):
        _fmt = '2I2HI'

        self.meta_type = struct.unpack('4b', buffer[:4])  # common, data, lock, format, size
        self._1, \
        self.offset, \
        self._2, \
        self._3, \
        self._4 = struct.unpack(_fmt, buffer[4:])


@dataclass
class ColorArray(tuple):
    color_array: tuple[ColorRGBA]

    @staticmethod
    def from_bytes(buffer: bytes) -> 'ColorArray':
        color_array = [ ColorRGBA( *struct.unpack('4B', rgba) ) for rgba in split_bytes(buffer, 4) ]
        return ColorArray(tuple(color_array))

    def compress(self, funcobj, **kwargs) -> 'ColorArray':
        compressed_color_table = []
        for color in self:
            r, g, b, a = funcobj( color.r, color.g, color.b, color.a, **kwargs )
            compressed_color_table += [ ColorRGBA(r, g, b, a) ]
        return ColorArray(tuple(compressed_color_table))

    def color_array2colortable_pixelarray(self: 'ColorArray') -> list[BMPColorTable, BMPPixelArray]:
        color_table, pixel_array = [], []

        for color in self.compress(round, coef=12):
            if color in color_table:
                pixel_array += [ color_table.index(color) ]
            else:
                color_table += [ color ]
                pixel_array += [ color_table.index(color) ]

        print(f'  {len(color_table)=}\n  {len(pixel_array)=}')

        return [ BMPColorTable(tuple(color_table)), BMPPixelArray(tuple(pixel_array)) ]


@dataclass(slots=True)
class ColorRGB:
    r: int
    g: int
    b: int


@dataclass(slots=True)
class ColorRGBA:
    r: int
    g: int
    b: int
    a: int


def xpr0_2_bmp_file(xpr0: XPR0) -> BMPFile:
    signature = 'BM'
    img_size = xpr0.file_size - xpr0.head_size
    img_width = int(np.sqrt(img_size))
    img_height = int(np.sqrt(img_size))

    ## bmpheader
    # file_size
    # pixel_array_offset
    bmp_header = BMPHeader(xpr0.file_size, 0, 0, xpr0.head_size)

    ## dib
    # image_width
    # image_height
    # image_size
    colors = len(xpr0.color_array)
    dib_header = DIBHeader(40, img_width, img_height, img_size, colors )

    ## get color table and pixel array, then add header
    color_table, pixel_array = xpr0.color_array.color_array2colortable_pixelarray()


    return BMPFile(
        signature,
        bmp_header,
        dib_header,
        color_table,
        pixel_array
    )


# def XPR02BMPHeader( file_size: int, pixel_array_offset: int ) -> BMPHeader:
#     return BMPHeader(
#         file_size,
#         0, 0,
#         pixel_array_offset
#     )


# def XPR02DIBHeader(xpr0: XPR0) -> DIBHeader:

#     return DIBHeader(
#         dib_header_size,
#         image_width,
#         image_height,
#         # planes,
#         # bits_per_pixel,
#         # compression,
#         image_size,
#         # unknown_1,
#         # unknown_2,
#         colors,
#         # imp_colors
#     )
