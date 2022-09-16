from __future__ import annotations

from typing import (
    BinaryIO
)
from dataclasses import (
    dataclass, 
    field
)

from lua_main import (
    Constants,
    Registers
)


@dataclass(slots=True)
class Instruction:
    A: int
    B: int
    Bx: int
    sBx: int
    C: int
    OP: int

    @staticmethod
    def bytes2Instruction(self, instruction: bytes):
        slices = (slice(0, 8),
                  slice(8, 17),
                  slice(8, 26),
                  slice(8, 26),
                  slice(17, 26),
                  slice(26, None))

        binary = bin(int.from_bytes(instruction, 'little'))[slice(2, None)].zfill(32)
        A, B, Bx, sBx, C, OP = ( int(binary[slc], 2) for slc in slices )
        return Instruction(A, B, Bx, sBx, C, OP)


@dataclass(slots=True)
class ByteCode:
    fo: BinaryIO
    constants: Constants
    registers: Registers
    
    def __iter__(self):
        return self.fo

    def Move(self):
        ''' 0
        Copy a value between registers '''
        ...

    def LoadK(self):
        ''' 1
        Load a constant into a register '''
        ...

    def LoadBool(self):
        ''' 2
        Load a boolean into a register '''
        ...

    def LoadNil(self):
        ''' 3
        Load nil values into a range of registers '''
        ...

    def GetUpVal(self):
        ''' 4
        Read an upvalue into a register '''
        ...

    def GetGlobal(self):
        ''' 5
        Read a global variable into a register '''
        ...

    def GetTable(self):
        ''' 6
        Read a table element into a register '''
        ...

    def SetGlobal(self):
        ''' 7
        Write a register value into a global variable '''
        ...

    def SetUpVal(self):
        ''' 8
        Write a register value into an upvalue '''
        ...

    def SetTable(self):
        ''' 9
        Write a register value into a table element '''
        ...

    def NewTable(self):
        ''' 10
        Create a new table '''
        ...

    def Self(self):
        ''' 11
        Prepare an object method for calling '''
        ...

    def Add(self):
        ''' 12
        Addition '''
        ...

    def Sub(self):
        ''' 13
        Subtraction '''
        ...

    def Mul(self):
        ''' 14
        Multiplication '''
        ...

    def Div(self):
        ''' 15
        Division '''
        ...

    def Pow(self):
        ''' 16
        Exponentiation '''
        ...

    def Unm(self):
        ''' 17
        Unary minus '''
        ...

    def Not(self):
        ''' 18
        Logical NOT '''
        ...

    def Concat(self):
        ''' 19
        Concatenate a range of registers '''
        ...

    def JMP(self):
        ''' 20
        Unconitional jump '''
        ...

    def EQ(self):
        ''' 21
        Equality test '''
        ...

    def LT(self):
        ''' 22
        Less than test '''
        ...

    def LE(self):
        ''' 23
        Less than or equal test '''
        ...

    def Test(self):
        ''' 24
        Test for short-circuit logical and and or evaluation '''
        ...

    def Call(self):
        ''' 25
        Call a closure '''
        ...

    def TailCall(self):
        ''' 26
        Perform a tail call '''
        ...

    def Return(self):
        ''' 27
        Return from from function call '''
        ...

    def ForLoop(self):
        ''' 28
        Iterate a numeric for loop '''
        ...

    def TForLoop(self):
        ''' 29
        Iterate a generic for loop '''
        ...

    def TForPrep(self):
        ''' 30
        Initialization for a generic for loop '''
        ...

    def SetList(self):
        ''' 31
        Set a range of array elements for a table '''
        ...

    def SetListTo(self):
        ''' 32
        Set a variable number of table elements '''
        ...

    def Close(self):
        ''' 33
        Close a range of locals being used as upvalues '''
        ...

    def Closure(self):
        ''' 34
        Create a closure of a function prototype '''
        ...
