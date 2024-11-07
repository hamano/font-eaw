#!/usr/bin/env python3
import fontforge
import psMat
from pprint import pprint

ASCENT = 1648
DESCENT = 400

def main():
    font_new = fontforge.font()
    font_new.encoding = "UnicodeFull"
    font_new.em = 2048
    font_new.ascent = ASCENT
    font_new.descent = DESCENT
    glyph = font_new.createChar(-1, "grid")
    glyph.width = 2024
    pen = glyph.glyphPen()
    width = 200
    offset_x = 500
    offset_y = 100

    pen.moveTo((0, offset_y))
    pen.lineTo((2048, offset_y))
    pen.lineTo((2048, ASCENT - DESCENT - offset_y))
    pen.lineTo((0, ASCENT - DESCENT - offset_y))
    pen.closePath()

    pen.moveTo((offset_x, -DESCENT))
    pen.lineTo((2048 - offset_x, -DESCENT))
    pen.lineTo((2048 - offset_x, ASCENT))
    pen.lineTo((offset_x, ASCENT))
    pen.closePath()

# grid
#    for i in range(0, 8, 2):
#        pen.moveTo((0, 200 * i + offset_y))
#        pen.lineTo((0, 200 * i + width + offset_y))
#        pen.lineTo((2048, 200 * i + width + offset_y))
#        pen.lineTo((2048, 200 * i + offset_y))
#        pen.closePath()
#        pen.moveTo((200 * i + offset_x, -200))
#        pen.lineTo((200 * i + width + offset_x, -200))
#        pen.lineTo((200 * i + width + offset_x, 2048))
#        pen.lineTo((200 * i + offset_x, 2048))
#        pen.closePath()

    glyph.removeOverlap()
    font_ja = fontforge.open('src/bizudgothic/BIZUDGothic-Regular.ttf')
    glyph = font_ja['glyph13070']
    glyph.transform(psMat.translate(0, -100))
    font_ja.selection.select('glyph13070')
    font_ja.copy()
    font_new.selection.select('grid')
    font_new.copy()
    font_new.selection.select(0x3000)
    font_new.paste()
    font_new[0x3000].exclude(glyph.layers[1])
    font_new.generate('src/custom/visible_space.ttf')

main()
