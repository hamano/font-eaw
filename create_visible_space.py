#!/usr/bin/env python3
import fontforge
from pprint import pprint

def main():
    font_new = fontforge.font()
    font_new.encoding = "UnicodeFull"
    font_new.em = 2048
    font_new.ascent = 1802
    font_new.descent = 246
    glyph = font_new.createChar(-1, "grid")
    glyph.width = 2024
    pen = glyph.glyphPen()
    width = 200
    offset_x = 300
    offset_y = 100
    for i in range(0, 8, 2):
        pen.moveTo((0, 200 * i + offset_y))
        pen.lineTo((0, 200 * i + width + offset_y))
        pen.lineTo((2048, 200 * i + width + offset_y))
        pen.lineTo((2048, 200 * i + offset_y))
        pen.closePath()
        pen.moveTo((200 * i + offset_x, -200))
        pen.lineTo((200 * i + width + offset_x, -200))
        pen.lineTo((200 * i + width + offset_x, 2048))
        pen.lineTo((200 * i + offset_x, 2048))
        pen.closePath()

    glyph.removeOverlap()
    font_ja = fontforge.open('src/bizudgothic/BIZUDGothic-Regular.ttf')
    #font_ja.selection.select('glyph13070')
    #font_ja.copy()
    font_new.selection.select('grid')
    font_new.copy()
    font_new.selection.select(0x3000)
    font_new.paste()
    font_new[0x3000].exclude(font_ja['glyph13070'].layers[1])
    font_new.generate('src/custom/visible_space.ttf')

main()
