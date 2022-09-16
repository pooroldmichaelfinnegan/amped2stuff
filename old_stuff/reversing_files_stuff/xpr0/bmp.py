
from dataclasses import dataclass
from typing import BinaryIO
import numpy as np
import io, struct

## local imports
from tools import (
    ColorRGBA,
    cls_from_bytes,
    split_bytes
)


_fmt_BMPHeader = 'I2HI'
_fmt_DIBHeader = '3I2H6I'


@dataclass
class BMPFile:
    signature: str
    bmp_header: 'BMPHeader'
    dib_header: 'DIBHeader'
    
    color_table: 'BMPColorTable'
    pixel_array: 'BMPPixelArray'
    
    @staticmethod
    def from_bitmap_file(fo: BinaryIO) -> 'BMPFile':
        signature = struct.unpack('2s', fo.read(2))
        bmp_header = cls_from_bytes(BMPHeader, fo.read(12), _fmt_BMPHeader)

        peek_dib_header_size, = struct.unpack('I', fo.peek()[:4])
        dib_header = cls_from_bytes(DIBHeader, fo.read(peek_dib_header_size), _fmt_DIBHeader)
        
        # assuming 8bit colors
        color_table = BMPColorTable.from_bytes(fo.read(dib_header.colors * 4))

        # pixel array
        pixel_array = BMPPixelArray.from_bytes(fo.read())

        return BMPFile(
            signature,
            bmp_header,
            dib_header,
            color_table,
            pixel_array,
        )
    def to_bytes(self) -> bytes:
        sig = bytes(self.signature, 'utf8')
        tmp1_bh_by = self.bmp_header.to_bytes()
        tmp1_dh_by = self.dib_header.to_bytes()
        tmp1_ct_by = self.color_table.to_bytes()
        tmp1_pa_by = self.pixel_array.to_bytes()
        tmp1_buf = sig + tmp1_bh_by + tmp1_dh_by + tmp1_ct_by + tmp1_pa_by

        tmp2_bh = self.bmp_header
        tmp2_dh = self.dib_header
        tmp2_ct = self.color_table
        tmp2_pa = self.pixel_array

        tmp2_bh.file_size = len(tmp1_buf)
        tmp2_bh.pixel_array_offset = len(sig + tmp1_bh_by + tmp1_dh_by + tmp1_ct_by)

        tmp2_dh.image_height = int(np.sqrt(len(tmp2_pa)))
        tmp2_dh.image_width = int(np.sqrt(len(tmp2_pa)))
        tmp2_dh.colors = len(tmp2_ct)
        tmp2_buf = sig + tmp2_bh.to_bytes() + tmp2_dh.to_bytes() + tmp2_ct.to_bytes() + tmp2_pa.to_bytes()

        return tmp2_buf



@dataclass(slots=True)
class BMPHeader:
    file_size: int
    reserved_1: int
    reserved_2: int
    pixel_array_offset: int

    def to_bytes(self):
        return struct.pack( _fmt_BMPHeader,
            self.file_size,          # 4 bytes
            self.reserved_1,         # 2 bytes
            self.reserved_2,         # 2 bytes
            self.pixel_array_offset  # 4 bytes
        )


@dataclass(slots=True)
class DIBHeader:
    dib_header_size: int
    image_width: int
    image_height: int
    # planes: int
    # bits_per_pixel: int
    # compression: int
    image_size: int
    # unknown_2: int
    colors: int
    # imp_colors: int

    def to_bytes(self):
        return struct.pack(
                _fmt_DIBHeader,
                self.dib_header_size,            # 4 bytes
                self.image_width,                # 4 bytes
                self.image_height,               # 4 bytes
                1,  ## self.planes,              # 2 bytes
                8,  ## self.bits_per_pixel,      # 2 bytes
                0,  ## self.compression,         # 4 bytes
                self.image_size,                 # 4 bytes
                0,  ## unknown                   # 4 bytes
                0,  ## unknown                   # 4 bytes
                self.colors,                     # 4 bytes
                self.colors  ## self.imp_colors  # 4 bytes
            )


@dataclass
class BMPColorTable(tuple):
    color_table: tuple[ColorRGBA]
    
    # def is_dupe(self, color: ColorRGBA) -> bool:
    #     return color in self
    @staticmethod
    def from_bytes(buffer: bytes) -> 'BMPColorTable':
        return BMPColorTable( tuple( ColorRGBA( *struct.unpack('4B', rgba) ) for rgba in split_bytes( buffer, 4 )))
    def to_bytes(self) -> bytes:
        return b''.join( rgba.to_bytes() for rgba in self.color_table )


@dataclass
class BMPPixelArray(tuple):
    pixel_array: tuple[int]

    @staticmethod
    def from_bytes(buffer: bytes) -> 'BMPPixelArray':
        return BMPPixelArray( struct.unpack( f'{len(buffer)}B', buffer ))
    def to_bytes(self) -> bytes:
        print(max(self.pixel_array))
        return b''.join( struct.pack('B', byte) for byte in self.pixel_array )
