#!/usr/bin/env python3
"""fonts.google.com から Noto Emoji を取得する

GitHub の google/fonts リポジトリは更新が遅れるため、
fonts.google.com のダウンロード用マニフェストから直接取得する。
"""
import json
import urllib.request

LIST_URL = 'https://fonts.google.com/download/list?family=Noto%20Emoji'
FILES = {
    'NotoEmoji-VariableFont_wght.ttf': 'NotoEmoji%5Bwght%5D.ttf',
    'OFL.txt': 'OFL.txt',
}


def fetch(url):
    with urllib.request.urlopen(url) as res:
        return res.read()


def main():
    body = fetch(LIST_URL).decode('utf-8')
    # 先頭の ")]}'" を除去
    manifest = json.loads(body[body.index('{'):])['manifest']

    for f in manifest['files']:
        if f['filename'] in FILES:
            with open(FILES[f['filename']], 'w') as out:
                out.write(f['contents'].replace('\r\n', '\n'))
            print(f"{FILES[f['filename']]}")

    for ref in manifest['fileRefs']:
        if ref['filename'] in FILES:
            with open(FILES[ref['filename']], 'wb') as out:
                out.write(fetch(ref['url']))
            print(f"{FILES[ref['filename']]}")


if __name__ == '__main__':
    main()
