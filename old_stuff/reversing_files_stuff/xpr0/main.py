import sys, io

## local imports
from bmp import BMPFile
from xpr0 import XPR0, xpr0_2_bmp_file


def main(path):
    with open(path, 'rb') as fo:
        xpr0 = XPR0(fo)
        bmp = xpr0_2_bmp_file(xpr0)
        # bitmap = BMPFile(fo)
        # print(bitmap.pixel_array)
        # print(len(bitmap.pixel_array))
    path_bmp = path[:-3] + 'bmp'
    with open(path_bmp, 'wb') as fo:
        fo.write(bmp.to_bytes())


if __name__ == '__main__':
    main(sys.argv[1])
