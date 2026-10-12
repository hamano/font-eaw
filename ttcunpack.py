#!/usr/bin/env python3
import sys
from fontTools.ttLib import TTCollection

OUT_DIR='src/iosevka/'

def main():
    path = sys.argv[1]
    for font in TTCollection(path).fonts:
        name = font['name'].getDebugName(4)
        print(f'unpack {name}')
        outfile = OUT_DIR + name.replace(' ', '-') + '.ttf'
        font.save(outfile)

main()
