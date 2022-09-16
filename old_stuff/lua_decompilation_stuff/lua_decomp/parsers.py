from struct import unpack
import re, struct

opcodes = ['MOVE', 'LOADK', 'LOADBOOL', 'LOADNIL', 'GETUPVAL', 'GETGLOBAL', 'GETTABLE', 'SETGLOBAL', 'SETUPVAL', 'SETTABLE', 'NEWTABLE', 'SELF', 'ADD', 'SUB', 'MUL', 'DIV', 'POW', 'UNM', 'NOT', 'CONCAT', 'JMP', 'EQ', 'LT', 'LE', 'TEST', 'CALL', 'TAILCALL', 'RETURN', 'FORLOOP', 'TFORLOOP', 'TFORPREP', 'SETLIST', 'SETLISTO', 'CLOSE', 'CLOSURE']


constants, constants_list = [], []


# def header_parser(data: bytes):
#     print(unpack(f'<B3s?9Bd', data))


def function_parser(data):
    global constants, constants_list

    temp = data
    # source_name_length = int.from_bytes(data[:4], 'little')
    # source_name = data[4:4+source_name_length-1]


    ''' function header '''
    name_size, = unpack(f'<i', temp[:4])
    # print(name_size)
    f = f'<{name_size}si4b'; fs = struct.calcsize(f)
    # print(f'\nHEAD\n  {temp[:4] = }\n  {f = }\n  {fs = }')
    name, line_defined, upvalues_size, params_size, is_vararg, max_stacksize \
        = unpack(f, temp[4:4+fs])
    temp = temp[4+fs:]
    # print(f'{name = }\n{line_defined = }\n{upvalues_size = }\n{params_size = }\n{is_vararg = }\n{max_stacksize = }')

    temp = temp[4:]  # these 4 bytes change for some reason on different lua5.0 binaries, maybe locals section comes before lines defined
                     # this code was written to parse the first version lua5.0 (lua 5.0.0?)


    ''' line defined '''
    lines_count, = unpack(f'<i', temp[:4])
    # print(f'{lines_count = }')
    f = f'<{lines_count}i'; fs = struct.calcsize(f)
    # print(f'\nLINES\n  {temp[:4] = }\n  {f = }\n  {fs = }')
    lines = unpack(f, temp[4:4+fs])
    # print(f'  {lines_count = }\n  {lines = }')
    temp = temp[4+fs:]


    ''' locals '''  # dont know why main function locals section isnt in gap1.lua
    ''' upvalues '''  # out of scope vars
    # print(f'locals = {temp[:0x10]}')


    ''' constants (k)'''
    # print(f'const = {temp[:0x10]}')

    constants_count, = unpack(f'<i', temp[:4])  # sizek
    temp = temp[4:]

    for i in range(constants_count):
        const_type, size, value = temp[:1], None, None

        # ''' size, string\0 '''
        match const_type:  #TSTRING
            case b'\x04':
                size, = unpack(f'<i', temp[1:5])
                offset = 1 + 4 + size

                value, = unpack(f'{size}s', temp[5:5+size])
                decoded_str = value[:-1].decode()
                # print(decoded_str)

                constants += [[const_type, size, decoded_str]]
                constants_list += [decoded_str]

                temp = temp[5+size:]

            # ''' double '''
            case b'\x03':  #TNUMBER
                size = 8
                offset = 1 + 0 + size
                value, = unpack(f'd', temp[1:offset])

                constants += [[const_type, value]]
                constants_list += [value]

                temp = temp[offset:]

            # ''' size, s \0 t \0 r \0 i \0 n \0 g \0 \0 '''
            case b'\x09':  #??
                size, = unpack(f'<i', temp[1:5])
                offset = 1 + 4 + size*2
                value = unpack(f'<{size}h', temp[5:offset])
                string = ''.join([chr(i) for i in value[:-1]])

                constants += [[const_type, string]]
                constants_list += [string]

                temp = temp[offset:]


    # for i in constants_list:
    #     print(i)   

    ''' function prototypes '''  # need to implement some recursion which calls this python function for all nested lua functions
    # print(f'func proto size = {temp[:0x4]}')
    temp = temp[4:]


    ''' code '''
    size, = unpack(f'<i', temp[:4])
    code_block = temp[4:]

    # print(temp)

    tables, reg = {}, [None for i in range(max_stacksize)]
    globals = {}

    for i in range(0, len(code_block), 4):
        b4 = code_block[i:i+4]

        # if type(b4) == int: b4 = b4.to_bytes(4, 'big')

        b = bin(int.from_bytes(b4, 'little'))[2:].zfill(32)
        A, B, C, op = int(b[:8], 2), int(b[8:17], 2), int(b[17:26], 2), int(b[26:], 2)
        Bx, sBx = int(b[8:26], 2), int(b[8:26], 2)
        # print(f'{len(reg) = }')
        # print(f'\n\n{A: 8}{B: 9}{C: 9}{Bx: 9}{op: 8}{opcodes[op]:>15}')
        # print(f'        {constants_list[A] = }\n        {constants_list[B%250] = }\n        {constants_list[C%250] = }')
        # print(f'{A: 8}{B: 9}{C: 9}{Bx: 9}{op: 8}{code_block[i:i+8]}'  )
        # print(constants_list)
        
        match opcodes[op]:
            case 'LOADK':  # 1   load constant into register list
                reg[A] = constants_list[Bx]
                # print(f'{A: 8}{B: 9}{C: 9}{Bx: 9}{op: 8}{opcodes[op]:>15}\n{reg}\n')

            case 'LOADBOOL':  # 2
                if not C: reg[A] = bool(B)
                else: print('LOADBOOL not implemented')

            case 'SETGLOBAL':  # 7
                globals[constants_list[A]] = reg[Bx]

            case 'SETTABLE':  # 9
                # print(f'{reg[A] = }  {B = }  {C = }\n')    
                # print(f'      {constants_list = }\n      {reg = }')
                if B <  250 >  C:
                    # print(f'      R[A] {reg[A]}\n      R[B] {reg[B]}\n      R[C] {reg[C]}')
                    reg[A].update({reg[B]: reg[C]})
                if B <  250 <= C:
                    # print(f'      R[A] {reg[A]}\n      R[B] {reg[B]}\n      K[C] {constants_list[C%250]}')
                    reg[A].update({reg[B]: constants_list[C%250]})
                if B >= 250 >  C:
                    # print(f'      R[A] {reg[A]}\n      K[B] {constants_list[B%250]}\n      R[C] {reg[C]}')
                    reg[A].update({constants_list[B%250]: reg[C]})
                else:
                    # print(f'      R[A] {reg[A]}\n      K[B] {constants_list[B%250]}\n      K[C] {constants_list[C%250]}')
                    reg[A].update({constants_list[B%250]: constants_list[C%250]})
            
        
            case 'NEWTABLE': reg[A] = {}  # 10

            case 'RETURN': pass  # 27

            case 'SETLIST':  # 31
                m = lambda a, x: slice(start := a + x-x%32 +1, start + x%32 +1)
                reg[A] = reg[m(A, Bx)]

                # print(f'        {m(A, Bx) = }')
                # print(f'        {reg[Bx] = }')
                # print()

    # print(f'{constants_list = }\n{reg = }\n')
    
    # for i, v in enumerate(reg):
    #     print(i, v if v is not None else '')

    # for k in reg:
    #     print(k)

    # for i in reg:
    #     [print(i), print([j for j in i])][type(i) == dict]
    
    # # print(reg)
    print(globals)
    # print(f'{constants_list = }')
    # # print() 
    # print(reg)
