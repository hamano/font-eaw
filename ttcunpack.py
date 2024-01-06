#!/usr/bin/env python3
import sys
import fontforge
import json

OUT_DIR='src/iosevka/'

def main():
    stats = {}
    path = sys.argv[1]
    names = fontforge.fontsInFile(path)
    for name in names:
        print(f'unpack {name}')
        font = fontforge.open(f'{path}({name})')
        outfile = OUT_DIR + name.replace(' ', '-') + '.ttf'
        font.generate(outfile)

main()
