#!/usr/bin/env python3
import sys
import click
import fontforge
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

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


def list_gsub(font, tag):
    gsub = font['GSUB'].table
    index = None
    for feature in gsub.FeatureList.FeatureRecord:
        if feature.FeatureTag == tag:
            index = feature.Feature.LookupListIndex[0]
    if index == None:
        print(f'{tag} LookupIndex notfound')
        return None
    lookup_wwid = gsub.LookupList.Lookup[index]
    mapping = {}
    for t in lookup_wwid.SubTable:
        mapping.update(t.ExtSubTable.mapping)
    cmap = font.getBestCmap()
    rmap = {v: k for k, v in cmap.items()}
    for n_name, w_name in mapping.items():
        code = rmap.get(n_name, -1)
        try:
            c = chr(code)
        except:
            c = ''
        print(f'U+{code:04X} {c} {n_name} -> {w_name}')

@cli.command()
@click.argument('filename')
def list_wwid(filename):
    font = TTFont(filename)
    list_gsub(font, 'WWID')

@cli.command()
@click.argument('filename')
def list_nwid(filename):
    font = TTFont(filename)
    list_gsub(font, 'NWID')

@cli.command()
@click.argument('filename')
def list_cmap(filename):
    font = TTFont(filename)
    #print('best', font.getBestCmap())
    for table in font['cmap'].tables:
        if not table.isUnicode():
            continue
        print(table.platformID, table.platEncID, table.language)

@cli.command()
@click.argument('filename')
def list_best_cmap(filename):
    font = TTFont(filename)
    cmap = font.getBestCmap()
    for code, name in cmap.items():
        print(f'{code:X} {name}')

@cli.command()
@click.argument('filename')
def list_fwid(filename):
    font = TTFont(filename)
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

@cli.command()
@click.option('--font', '-f', default='build/EAW-CONSOLE-Regular.ttf')
@click.argument('text')
def draw(font, text):
    font_size = 64
    width, height = font_size * 2, font_size
    COLOR_WHITE=(0xFF, 0xFF, 0xFF)
    COLOR_BLACK=(0, 0, 0)
    image = Image.new('RGB', (width, height), color=COLOR_WHITE)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font, font_size)
    ret = draw.text((0, 0), text, font=font, fill=COLOR_BLACK)
    image = image.quantize(8)
    image.save("draw.png")
    image.show()

def main():
    cli()

main()
