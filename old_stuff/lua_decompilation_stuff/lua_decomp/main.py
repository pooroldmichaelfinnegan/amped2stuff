import sys

from parsers import *

with open(str(sys.argv[1]), 'rb') as lua_:
    lua = lua_.read()

# with open('../../../amped_/amped_extracted_/Characters/boarder/boarder_res/def/net.boarder', 'rb') as lua_buf:
#     lua = lua_buf.read()



''' gap1.lua stuff'''
# code = lua[0x24F:]


header = lua[:0x16]
main_function_section = lua[0x16:]

# code_parser(code)
# header_parser(header)
function_parser(main_function_section)


# print(f'-- CONSTANTS LIST --')
# for i in constants_list:
#     print(i)

# for i, c in enumerate(constants_list):
#     print(i+250, c)
