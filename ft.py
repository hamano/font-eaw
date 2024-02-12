#!/usr/bin/env python3
import sys
import fontforge
from fontTools.ttLib import TTFont

def list_glyph():
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

def list_cmap():
    path = sys.argv[1]
    font = TTFont(path)
    print('best', font.getBestCmap())
    for table in font['cmap'].tables:
        if not table.isUnicode():
            continue
        print(table)
        print(table.platformID, table.platEncID, table.language)

def list_fwid():
    path = sys.argv[1]
    font = TTFont(path)
    gsub = font['GSUB'].table
    hmtx = font['hmtx']
    for feature in gsub.FeatureList.FeatureRecord:
        if feature.FeatureTag == 'fwid':
            index = feature.Feature.LookupListIndex[0]
            break

    lookup = gsub.LookupList.Lookup[index]
    mapping = lookup.SubTable[0].mapping
    for name in mapping.keys():
        new_name = mapping[name]
        print(name, hmtx[name], new_name, hmtx[new_name])

def main():
    list_glyph()

main()
