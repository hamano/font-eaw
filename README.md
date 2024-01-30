# East Asian Widthフォント

このフォントはターミナルで上で起こるEast Asian Width問題を緩和し、
文字が自然に表示されることをコンセプトとした合成フォントです。

East Asian Width問題はLinuxのターミナル表示が壊れる厄介な問題です。
これを解決するための[修正ロケール](https://github.com/hamano/locale-eaw)を公開していますが
フォントに依存して不自然な表示となるのでフォントも作る必要がありました。

[locale-eaw](https://github.com/hamano/locale-eaw)との組み合わせにより、glibcロケール、シェル、ターミナル、テキストエディタ、フォントの全ての文字幅を一致させることでターミナル作業が快適になります。

# フォントにまつわるEAW問題
- 狭くなる
- 右端が切れる
- 重なる
- 重ならないがスペースの後置が必要

[locale-eaw](https://github.com/hamano/locale-eaw)とこのフォントの組み合わせによって上記の問題を修正します。

# 合成フォント

このフォントは以下のフォントを合成しています。
- Iosevka Curly
- BIZ UDGothic
- Nerd Fonts
- Noto Emoji

# 特徴

- 視認性の高いプログラミング、ターミナル作業向けフォント
- Regular, Bold, Italic, BoldItalicの4書体
- 見える全角スペース
- 絵文字、NerdFontを幅広くサポート
- East Asian Width問題により、文字が潰れない、重ならない

このフォントは以下のフレーバーを提供します。

## EAW-FULLWIDTH
East Asian Ambisious Width文字をすべて全角にしたフォント

## EAW-CONSOLE
AmbiguousとNeutralの文字幅を個別に裁定

- 半角にしないとTUIが壊れる文字は半角(罫線・ブロック)
- 日本語圏で全角として扱われることが多い文字は全角(例※①)
- NerdFontのプライベート領域を全角
- 半角で描画することが困難な絵文字を全角

とした修正ロケールに適合するフォントです。

## EAW-FULLWIDTH
East Asian Ambisious Width文字をすべて全角にしたフォント
Ambisious Widthを全角に統一するなど、古典的なアプリケーションで利用できます。

### サンプル

![EAW-CONSOLEのサンプル画像](./sample/sample.png)

