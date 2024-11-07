import sys
import math
import json
import util
from functools import cache
from pprint import pprint
import fontforge
import psMat
from fontTools.ttLib import TTCollection
from fontTools.ttLib import TTFont
from fontTools.subset import Subsetter, Options
from fontTools.varLib import instancer
from fontTools.merge import Merger
import tomllib

DOIT_CONFIG = {
    'verbosity': 2,
}

with open("pyproject.toml", "rb") as f:
    pyproject = tomllib.load(f)

def expand_list(range_list):
    ret = []
    for code_range in range_list:
        token = code_range.split('..')                                                        
        if len(token) == 1:
            start = int(token[0].removeprefix('U+'), 16)
            ret.append(start)
        elif len(token) == 2:
            start = int(token[0].removeprefix('U+'), 16)
            end = int(token[1].removeprefix('U+'), 16)
            ret.extend(range(start, end + 1))
    return ret

def get_wwid_mapping(font):
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
    return mapping

def get_nwid_mapping(font):
    gsub = font['GSUB'].table
    index = None
    for feature in gsub.FeatureList.FeatureRecord:
        if feature.FeatureTag == 'NWID':
            index = feature.Feature.LookupListIndex[0]
    if index == None:
        print('NWID LookupIndex notfound')
        return None
    lookup_wwid = gsub.LookupList.Lookup[index]
    mapping = lookup_wwid.SubTable[0].ExtSubTable.mapping
    return mapping

def update_cmap(font, code, name):
    for table in font['cmap'].tables:
        if not table.isUnicode():
            continue
        if code in table.cmap:
            table.cmap[code] = name

def towide(font, mapping, code):
    cmap = font.getBestCmap()
    if code not in cmap:
        #print(f'U+{code:04X} not found in cmap')
        return
    name = cmap[code]
    if name not in mapping:
        #print(f'{name} U+{code:04X} not found in wwid_mapping')
        return
    wide_name = mapping[name]
    #print(f'towide U+{code:04X} {wide_name}')
    update_cmap(font, code, wide_name)


def iosevka_subset(flavor, style, task):
    font = TTFont(list(task.file_dep)[0])
    cmap = font.getBestCmap()
    update_cmap(font, ord('*'), 'asterisk.VSAB-3')
    update_cmap(font, ord('%'), 'percent.VSAO-3')
    update_cmap(font, ord('0'), 'zero.cv10-4')
    update_cmap(font, ord('1'), 'one.cv01-3')
    update_cmap(font, ord('7'), 'seven.cv07-2')
    update_cmap(font, ord('l'), 'l.cv47-4')
    update_cmap(font, ord('Z'), 'Z.cv35-2')
    update_cmap(font, ord('z'), 'uni1D22.cv35-2')

    # ワイド幅を持つグリフのマッピング
    wwid_mapping = get_wwid_mapping(font)

    # ロケールファイルに基づいてグリフ幅を修正
    wide_list = []
    if flavor == 'CONSOLE':
        locale = util.load_console_locale()
        for code in cmap.keys():
            if util.wcwidth(locale, code) == 2:
                wide_list.append(code)
    elif flavor == 'FULLWIDTH':
        locale = util.load_fullwidth_locale()
        for code in cmap.keys():
            if util.wcwidth(locale, code) == 2:
                wide_list.append(code)

    for code in wide_list:
        towide(font, wwid_mapping, code)

    options = Options()
    options.no_subset_tables.append('FFTM')
    subsetter = Subsetter(options=options)
    unicodes = set(cmap.keys())

    # 削除するグリフ
    remove_list = expand_list([
        'U+2028..U+2029', # LINE SEPARATOR,PARAGRAPH SEPARATOR
        'U+203B', # ※ JPフォントを利用
        'U+2121', # ℡ JPフォントを利用
        'U+2329..U+232A', # 〈〉EAW=Wなのに半角なので削除
        'U+25C6..U+25C7', # ◆◇JPフォントを利用
        'U+2605..U+2606', # ★☆JPフォントを利用
        'U+26A1', # ⚡EAW=Wなのに半角なので削除
        'U+26B2', # ⚲EAW=Wなのに半角なので削除
        'U+263F..U+2642', # ☿♀♁♂
        'U+2B55', # ⭕EAW=Wなのに半角なので削除
        'U+E0A0..U+E0D7', # NFカバー範囲
        'U+EF01..U+EF10', # NFカバー範囲
        'U+1F16A..U+1F16C', # 🅪🅫🅬絵文字領域で半角なので削除
    ])
    if flavor == 'CONSOLE':
        remove_list.extend(expand_list([
            'U+2690..U+2691', # ⚐⚑
            'U+213B', # ℻ JPフォントを利用
        ]))
    elif flavor == 'FULLWIDTH':
        # 予め調べておいた日本語フォントを優先するリスト
        with open('./eaw-fullwidth-ja.json', 'r') as f:
            ja_list = json.load(f)
        remove_list.extend(expand_list(ja_list))
    for code in remove_list:
        unicodes.discard(code)

    subsetter.populate(unicodes=unicodes)
    subsetter.subset(font)
    font.save(task.targets[0])


def task_iosevka_subset():
    """Iosevkaの各種スタイルを生成"""
    flavors = ['CONSOLE', 'FULLWIDTH']
    styles = ['Regular', 'Bold', 'Italic', 'BoldItalic']
    filenames = {
        'Regular': 'IosevkaTermCurly-Regular.ttf',
        'Bold': 'IosevkaTermCurly-Bold.ttf',
        'Italic': 'IosevkaTermCurlySlab-Italic.ttf',
        'BoldItalic': 'IosevkaTermCurlySlab-BoldItalic.ttf',
    }

    for flavor in flavors:
        for style in styles:
            font_file = filenames.get(style)
            yield {
                'name': f'{flavor}-{style}',
                'actions': [(iosevka_subset, [flavor, style])],
                'file_dep': [f'src/iosevka/{font_file}'],
                'targets': [f'build/IO-{flavor}-{style}-subset.ttf'],
                'clean': True,
            }


def iosevka_fixup(flavor, style, task):
    font_file = list(task.file_dep)[0]
    font = fontforge.open(font_file)

    # dereference
    for glyph in font.glyphs():
        glyph.unlinkRef()

    for glyph in font.glyphs():
        # add "io-" prefix
        glyph.glyphname = f"io-{glyph.glyphname}"
        if glyph.width == 500:
            resize_width = 1024
            scale = resize_width / glyph.width
            matrix = psMat.scale(scale, scale)
            glyph.transform(matrix)
        elif glyph.width == 1000:
            resize_width = 2048
            scale = resize_width / glyph.width
            matrix = psMat.scale(scale, scale)
            glyph.transform(matrix)

    # 半角を全角に引き伸ばし
    wide_list = expand_list([
        'U+2630..U+2637', # TRIGRAM Unicode 16でWide
        'U+268A..U+268F', # MONOGRAM Unicode 16でWide
        'U+4DC0..U+4DFF', # HEXAGRAM Unicode 16でWide
        'U+1D300..U+1D356', # MONOGRAM Unicode 16でWide
    ])
    if flavor == 'FULLWIDTH':
        # TODO: jaフォントを使ったほうが良いものもある
        wide_list.extend(expand_list([
            'U+2660..U+2661', 'U+2663..U+2665', 'U+2667', # CARD SUIT
            'U+2669', 'U+266C', # ♩♬
            'U+EE00..U+EE05', # progress
        ]))
    if flavor == 'CONSOLE':
        wide_list.extend(expand_list([
            'U+2180..U+2182', # ↀↁↂ
        ]))
    for code in wide_list:
        if code not in font:
            continue
        glyph = font[code]
        if glyph.width != 1024:
            continue
        resize_width = 2048
        scale = resize_width / glyph.width
        matrix = psMat.scale(scale, 1)
        glyph.transform(matrix)

    # 半角に縮小
    if flavor == 'FULLWIDTH':
        half_list = expand_list([
            'U+27F5..U+27FF', 'U+2B33', # ⟵〜⟿Neutralなので半角に
        ])
        for code in half_list:
            glyph = font[code]
            glyph.transform(psMat.scale(0.5, 1))

    # 全角にして中央寄せ
    wide_move_list = []
    if flavor == 'FULLWIDTH':
        # TODO: jaフォントを使ったほうが良いものもある
        with open('./eaw-fullwidth-wide.json', 'r') as f:
            wide_move_list.extend(expand_list(json.load(f)))

    # 全角に広げて中央寄せ
    for code in wide_move_list:
        if code not in font:
            continue
        glyph = font[code]
        bbox = glyph.boundingBox()
        bbwidth = bbox[2] - bbox[0]
        if bbwidth == 0:
            continue
        glyph.left_side_bearing = int((2048 - bbwidth) / 2)
        glyph.right_side_bearing = int(2048 - bbwidth - glyph.left_side_bearing)
        glyph.width = 2048

    font.ascent = 1802
    font.descent = 246
    font.generate(task.targets[0])
    font.close()


def task_iosevka_fixup():
    """Iosevkaの調整"""
    flavors = ['CONSOLE', 'FULLWIDTH']
    styles = ['Regular', 'Bold', 'Italic', 'BoldItalic']
    for flavor in flavors:
        for style in styles:
            yield {
                'name': f'{flavor}-{style}',
                'actions': [(iosevka_fixup, [flavor, style])],
                'file_dep': [f'build/IO-{flavor}-{style}-subset.ttf'],
                'targets': [f'build/IO-{flavor}-{style}.ttf'],
                'clean': True,
            }


def bizud_subset(flavor, style, task):
    font_file = list(task.file_dep)[0]
    font = TTFont(font_file)
    del font['DSIG']
    del font['meta']

    options = Options()
    subsetter = Subsetter(options=options)
    subsetter.glyph_names = task_nerdfont_subset
    unicodes = set(font.getBestCmap().keys())

    # latin文字を削除
    for code in range(0x0000, 0x02AF + 1):
        unicodes.discard(code)
    # 音符を削除(一貫性のため)
    for code in range(0x2669, 0x266F + 1):
        unicodes.discard(code)
    # ℡(U+2121)の変更
    font['glyf']['uni2121'] = font['glyf']['glyph13056']
    subsetter.populate(unicodes=unicodes)
    subsetter.subset(font)

    font.save(task.targets[0])
    font.close()


def task_bizud_subset():
    """BIZUDのサブセット"""
    flavors = ['CONSOLE', 'FULLWIDTH']
    styles = ['Regular', 'Bold', 'Italic', 'BoldItalic']
    filenames = {
        'Regular': f'src/bizudgothic/BIZUDGothic-Regular.ttf',
        'Bold': f'src/bizudgothic/BIZUDGothic-Bold.ttf',
        'Italic': f'src/bizudmincho/BIZUDMincho-Regular.ttf',
        'BoldItalic': f'src/bizudmincho/BIZUDMincho-Bold.ttf',
    }
    for flavor in flavors:
        for style in styles:
            filename = filenames.get(style)
            yield {
                'name': f'{flavor}-{style}',
                'actions': [(bizud_subset, [flavor, style])],
                'file_dep': [filename],
                'targets': [f'build/JA-{flavor}-{style}-subset.ttf'],
                'clean': True,
            }


def bizud_fixup(flavor, style, task):
    font_file = list(task.file_dep)[0]
    font = fontforge.open(font_file)

    for glyph in font.glyphs():
        # dereference
        glyph.unlinkRef()
        # add "nf-" prefix
        glyph.glyphname = f"ja-{glyph.glyphname}"
        # USフォントと調和させるため、ascentは1802から1648に変更される。
        # BBの高い漢字がascentに収まらければならない
        # 轟などの大きい漢字が収まっていればOK
        # TODO: 検証スクリプトを作る
        glyph.transform(psMat.translate(0, -100))

    # 半角に縮小
    if flavor == 'FULLWIDTH':
        half_list = expand_list([
            'U+2318', # ⌘ Neutralなので半角に
            'U+2601..U+2603', # ☁☂☃ Neutralなので半角に
            'U+2616..U+2617', # ☖☗ Neutralなので半角に
        ])
        for code in half_list:
            glyph = font[code]
            glyph.transform(psMat.scale(0.5, 1))

    if style.endswith('Italic'):
        angle = 9
        font.italicangle = -angle
        for glyph in font.glyphs():
           matrix = psMat.skew(math.radians(angle))
           glyph.transform(matrix)

    #font.ascent = 1802
    #font.descent = 246
    font.save(task.targets[0])
    font.close()


def task_bizud_fixup():
    """BizUDの調整"""
    flavors = ['CONSOLE', 'FULLWIDTH']
    styles = ['Regular', 'Bold', 'Italic', 'BoldItalic']
    for flavor in flavors:
        for style in styles:
            font_file = f'build/JA-{flavor}-{style}-subset.ttf'
            yield {
                'name': f'{flavor}-{style}',
                'actions': [(bizud_fixup, [flavor, style])],
                'file_dep': [font_file],
                'targets': [f'build/JA-{flavor}-{style}.ttf'],
                'clean': True,
            }


def nerdfont_subset(task):
    font_file = list(task.file_dep)[0]
    font = TTFont(font_file)
    del font['PfEd'] # 不要なテーブル
    options = Options()
    subsetter = Subsetter(options=options)
    unicodes = set(font.getBestCmap().keys())
    subsetter.populate(unicodes=unicodes)
    subsetter.subset(font)

    font.save(task.targets[0])
    font.close()


def task_nerdfont_subset():
    """NerdFontのサブセット"""
    return {
        'actions': [nerdfont_subset],
        'file_dep': ['src/nerdfont/SymbolsNerdFontMono-Regular.ttf'],
        'targets': ['build/NF-subset.ttf'],
        'clean': True,
    }


def nerdfont_fixup(task):
    font_file = list(task.file_dep)[0]
    font = fontforge.open(font_file)
    for glyph in font.glyphs():
        # add "nf-" prefix
        glyph.glyphname = f"nf-{glyph.glyphname}"
    font.save(task.targets[0])
    font.close()


def task_nerdfont_fixup():
    """NerdFontの調整"""
    return {
        'actions': [nerdfont_fixup],
        'file_dep': ['build/NF-subset.ttf'],
        'targets': ['build/NF.ttf'],
        'clean': True,
    }


def notoemoji_subset(style, task):
    weights = {
        'Regular': 400,
        'Bold': 700
    }
    wght = weights[style]
    font_file = list(task.file_dep)[0]
    font = TTFont(font_file)
    options = Options()
    subsetter = Subsetter(options=options)
    unicodes = set(font.getBestCmap().keys())
    remove_code = expand_list([
        'U+2654..U+265F', # チェス駒が揃ってないので削除
        'U+2660..U+2667', # CARD SUITが揃ってないので削除
    ])
    # remove code
    for code in remove_code:
        unicodes.discard(code)

    subsetter.populate(unicodes=unicodes)
    subsetter.subset(font)
    font_new = instancer.instantiateVariableFont(font, {"wght": wght})
    del font_new['STAT']
    font_new.save(task.targets[0])


def task_notoemoji_subset():
    """NotoEmojiのサブセットを生成"""
    styles = ['Regular', 'Bold']
    for style in styles:
        yield {
            'name': style,
            'actions': [(notoemoji_subset, [style])],
            'file_dep': ['src/notoemoji/NotoEmoji%5Bwght%5D.ttf'],
            'targets': [f'build/NE-{style}-subset.ttf'],
            'clean': True,
        }


def notoemoji_fixup(flavor, task):
    font_file = list(task.file_dep)[0]
    font = fontforge.open(font_file)

    # dereference
    for glyph in font.glyphs():
        glyph.unlinkRef()

    resize_width = 2048
    for glyph in font.glyphs():
        # add "ne-" prefix
        glyph.glyphname = f"ne-{glyph.glyphname}"
        if glyph.width != 0:
            scale = resize_width / glyph.width
            matrix = [scale, 0, 0, scale, 0, 0]
            glyph.transform(matrix)

    if flavor == 'CONSOLE':
        half_list = expand_list([
            'U+2744', # ❄ Neutralなので半角に
            'U+2747', # ❇ Neutralなので半角に
            'U+2763', # ❣ Neutralなので半角に
        ])
        for code in half_list:
            glyph = font[code]
            glyph.transform(psMat.scale(0.5, 1))

    if flavor == 'FULLWIDTH':
        locale = util.load_fullwidth_locale()
        for glyph in font.glyphs():
            if glyph.unicode < 0:
                continue
            width = util.wcwidth(locale, glyph.unicode)
            if glyph.width == 2048 and width == 1:
                # 半角に縮小
                glyph.left_side_bearing = 0
                glyph.right_side_bearing = 0
                bbox = glyph.boundingBox()
                bbwidth = bbox[2] - bbox[0]
                if bbwidth == 0:
                    continue
                scale = 1024.0 / bbwidth
                glyph.transform(psMat.scale(scale, 1))
                glyph.width = 1024

    font.save(task.targets[0])
    font.close()

def task_notoemoji_fixup():
    """NotoEmojiの調整"""
    flavors = ['CONSOLE', 'FULLWIDTH']
    styles = ['Regular', 'Bold']
    for flavor in flavors:
        for style in styles:
            yield {
                'name': f'{flavor}-{style}',
                'actions': [(notoemoji_fixup, [flavor])],
                'file_dep': [f'build/NE-{style}-subset.ttf'],
                'targets': [f'build/NE-{flavor}-{style}.ttf'],
                'clean': True,
            }


def merge_font(target, path, unicodes=None, overwrite=False):
    source = fontforge.open(path)
    if unicodes == None:
        unicodes = []
        for glyph in source.glyphs():
            if glyph.unicode == -1:
                continue
            unicodes.append(glyph.unicode)

    for unicode in unicodes:
        #print(f"U+{unicode:0X}")
        if not overwrite:
            if unicode in target:
                continue
        if unicode not in source:
            continue
        glyph = source[unicode]
        new_glyph = target.createChar(glyph.unicode, glyph.glyphname)
        new_glyph.comment = glyph.comment
        new_glyph.foreground = glyph.foreground
        if glyph.background:
            print('background')
            sys.exit()

        new_glyph.width = glyph.width
        new_glyph.vwidth = glyph.vwidth

        for anchor in glyph.anchorPoints:
            if anchor[1] == 'ligature':
                new_glyph.addAnchorPoint(anchor[0], anchor[1], anchor[2], anchor[3], anchor[4])
            else:
                new_glyph.addAnchorPoint(anchor[0], anchor[1], anchor[2], anchor[3])

    source.close()


def ttf(flavor, style, font_list, task):
    font = fontforge.font()
    font.familyname = f"EAW {flavor}"
    font.fontname = f"EAW{flavor}-{style}"
    font.fullname = f"EAW {flavor} {style}"
    font.version = pyproject['tool']['poetry']['version']
    font.encoding = "UnicodeFull"
    font.copyright = open('COPYING').read().format(font.familyname)
    font.em = 2048
    font.ascent = 1648
    font.descent = 400
    font.weight = style
    for f in font_list:
        merge_font(font, f)
    font.generate(task.targets[0]) 
    font.close()
    # postテーブルを編集
    font = TTFont(task.targets[0])
    font['post'].isFixedPitch = 1
    # OS/2テーブルを編集
    font['OS/2'].usWinAscent = 1648
    font['OS/2'].usWinDescent = 400
    font['OS/2'].sTypoLineGap = 0
    font['OS/2'].xAvgCharWidth = 1024
    font['OS/2'].panose.bProportion = 3
    # hheaテーブルを編集
    font['hhea'].ascent = 1648
    font['hhea'].descent = -400
    font['hhea'].lineGap = 0
    font.save(task.targets[0])
    font.close()


def task_ttf():
    """フォント生成"""
    flavors = ['CONSOLE', 'FULLWIDTH']
    styles = ['Regular', 'Bold', 'Italic', 'BoldItalic']
    for flavor in flavors:
        for style in styles:
            font_list = [
                f'build/IO-{flavor}-{style}.ttf',
                'src/custom/visible_space.ttf',
                f'build/JA-{flavor}-{style}.ttf',
                'build/NF.ttf',
            ]
            if style.startswith('Bold'):
                font_list.append(f'build/NE-{flavor}-Bold.ttf')
            else:
                font_list.append(f'build/NE-{flavor}-Regular.ttf')
            yield {
                'name': f'{flavor}-{style}',
                'actions': [(ttf, [flavor, style, font_list])],
                'file_dep': font_list,
                'targets': [f'build/EAW-{flavor}-{style}.ttf'],
                'clean': True,
            }


def stats(task):
    font_file = list(task.file_dep)[0]
    stats = util.stats_font(font_file)
    with open(task.targets[0], 'w') as f:
        for k, v in stats:
            print(k, v, file=f)


def task_stats():
    """統計ファイル生成"""
    flavors = ['CONSOLE', 'FULLWIDTH']
    styles = ['Regular']
    for flavor in flavors:
        for style in styles:
            font_list = [f'build/EAW-{flavor}-{style}.ttf']
            yield {
                'name': f'{flavor}-{style}',
                'actions': [(stats, [])],
                'file_dep': font_list,
                'targets': [f'stats/EAW-{flavor}-{style}.txt'],
            }


def ttc(flavor, font_list, task):
    fonts = [fontforge.open(font_file) for font_file in font_list]
    fonts[0].generateTtc(task.targets[0], fonts[1:], layer=1)


def task_ttc():
    """TTC生成"""
    flavors = ['CONSOLE', 'FULLWIDTH']
    styles = ['Regular', 'Bold', 'Italic', 'BoldItalic']
    for flavor in flavors:
        font_list = []
        for style in styles:
            font_list.append(f'build/EAW-{flavor}-{style}.ttf')
        yield {
            'name': f'{flavor}',
            'actions': [(ttc, [flavor, font_list])],
            'file_dep': font_list,
            'targets': [f'build/EAW-{flavor}.ttc'],
            'clean': True,
        }


def task_all():
    """全てを生成"""
    return {
        'actions': None,
        'task_dep': ['ttc', 'stats']
    }
