#!/usr/bin/env python3
import sys
import click
import fontforge
from fontTools.ttLib import TTFont

@click.group()
def cli():
    pass

@cli.command()
@click.argument('filename')
def list_glyph(filename):
    path = sys.argv[1]
    font = fontforge.open(filename)
    for g in font.glyphs():
        if g.unicode == 0:
            continue
        try:
            c = chr(g.unicode)
        except ValueError:
            c = '?'
        print(f'{g.glyphname} {g.originalgid} U+{g.unicode:04X} {g.width} {c}')


@cli.command()
@click.argument('filename')
def list_wwid(filename):
    font = TTFont(filename)
    gsub = font['GSUB'].table
    index = None
    for feature in gsub.FeatureList.FeatureRecord:
        if feature.FeatureTag == 'WWID':
            index = feature.Feature.LookupListIndex[0]
    if index == None:
        print('WWID LookupIndex notfound')
        return None
    lookup_wwid = gsub.LookupList.Lookup[index]
    mapping = lookup_wwid.SubTable[0].ExtSubTable.mapping
    cmap = font.getBestCmap()
    rmap = {v: k for k, v in cmap.items()}
    #print(rmap)
    for n_name, w_name in mapping.items():
        code = rmap.get(n_name, -1)
        try:
            c = chr(code)
        except:
            c = ''
        print(f'U+{code:04X} {c} {n_name} -> {w_name}')

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
    cli()

main()