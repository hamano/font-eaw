import fontforge
import json
def load_width_from_json(path):
    width_map = {}
    with open(path, 'r') as f:
        width_list = json.load(f)
        return width_list

def load_locale(path):
    width_list = []
    with open(path, 'rt', encoding='utf-8') as f:
        state = 0
        for line in f.readlines():
            if line.startswith('WIDTH'):
                state = 1
                continue
            if line.startswith('END WIDTH'):
                state = 0
                continue
            if state == 0:
                continue
            if line.startswith('%'):
                continue
            (code, width) = line.split()
            width = int(width)
            if '...' in code:
                (start, end) = code.split('...')
                start = int(start.strip('<U>'), 16)
                end = int(end.strip('<U>'), 16)
                width_list.append((start, end, width))
            else:
                code = int(code.strip('<U>'), 16)
                width_list.append((code, code, width))
    return width_list

def wcwidth(width_list, code):
    for (start, end, width) in width_list:
        if start <= code <= end:
            return width
    return 1

def check_width(width_file, font_file):
    width_list = load_locale(width_file)
    font = fontforge.open(font_file)
    error = 0
    for glyph in font.glyphs():
        if glyph.unicode < 0x20:
            continue
        width = wcwidth(width_list, glyph.unicode)
        if width * 1024 != glyph.width:
            if width == 0:
                # COMBININGについては無視
                continue
            print(
                    f'[{chr(glyph.unicode)}] U+{glyph.unicode:04X} width is wrong.'
                    f' width: {width}'
                    f' glyph.width: {glyph.width}'
                  )
            error += 1
    return error

