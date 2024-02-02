#!/usr/bin/env python3
import sys
import fontforge
import json

def main():
    path = sys.argv[1]
    font = fontforge.open(path)
    for g in font.glyphs():
        if g.unicode == 0:
            continue
        try:
            c = chr(g.unicode)
        except ValueError:
            c = '?'
        print(f'{g.glyphname} {g.originalgid} U+{g.unicode:04X} {g.width} {c}')

main()
