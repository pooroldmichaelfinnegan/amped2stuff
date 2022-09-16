from __future__ import annotations


from dataclasses import dataclass
from typing import (
    BinaryIO,
    Generator
)
import struct

## local imports
from bytecode import ByteCode, Code


__all__ = [
    ''
]

class MainFunc:
    def __init__(self, fo: BinaryIO):
        g: Generator = GEN()
        
        while fo.peek():
            next(g)(fo)


class FuncHeader:
    def __init__(self, fo: BinaryIO):
        self.func_name_size: int = struct.unpack('I', fo.read(4))[0]
        self.name, \
        self.line_defined, \
        self.upvalues_size, \
        self.params_size, \
        self.is_vararg, \
        self.max_stacksize \
            = struct.unpack(F:=f'{self.func_name_size}sI4b', fo.read(struct.calcsize(F)))


class LineDefined(list):
    def __init__(self, fo: BinaryIO):
        self.num: int = struct.unpack('I', fo.read(4))[0]
        self += list(struct.unpack(F:=f'{self.num}I', fo.read(struct.calcsize(F))))

class Locals:
    def __init__(self, fo: BinaryIO):
        ...


class UpValues:
    def __init__(self, fo: BinaryIO):
        ...


class Constants(list):
    def __init__(self, fo: BinaryIO):
        self.num: int = struct.unpack('I', fo.read(4))[0]
        self.constant_type = { b'\x03': self.double,
                               b'\x04': self.string,
                               b'\x09': self.null_separated_string }
        self += [ self.constant_type[fo.read(1)](fo) for _ in range(self.num) ]
    def double(self, fo: BinaryIO) -> float:
        return struct.unpack(F:='d', fo.read(struct.calcsize(F)))[0]
    def string(self, fo: BinaryIO) -> str:
        return struct.unpack(F:=f'{struct.unpack("I", fo.read(4))[0]-1}sx', fo.read(struct.calcsize(F)))[0]
    def null_separated_string(self, fo: BinaryIO) -> str:
        string_length: int = int.from_bytes(fo.read(4), 'little')
        string_length_in_bytes: int = string_length * 2
        buffer: bytes = fo.read(string_length_in_bytes)
        mutable_buffer: bytearray = bytearray(buffer)
        null_terminator: bytearray = mutable_buffer.remove(0)
        to_string: str = null_terminator.decode()
        return to_string


class FuncPrototypes:
    def __init__(self, fo: BinaryIO):
        self.num = fo.read(4)


class Registers(list):
    ...


def GEN() -> object:
    yield FuncHeader
    yield LineDefined
    yield Locals
    yield UpValues
    yield Constants
    yield FuncPrototypes
    yield ByteCode
