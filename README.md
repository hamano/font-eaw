# East Asian Widthフォント

このフォントはターミナルで上で起こるEast Asian Width問題を緩和し、
文字が自然に表示されることをコンセプトとした合成フォントです。

East Asian Width問題はLinuxのターミナル表示が壊れる厄介な問題です。
これを解決するための[修正ロケール](https://github.com/hamano/locale-eaw)を公開していますが
フォントに依存して不自然な表示となるのでフォントも調整する必要がありました。

[locale-eaw](https://github.com/hamano/locale-eaw)との組み合わせにより、glibcロケール、シェル、ターミナル、テキストエディタ、フォントの全ての文字幅を一致させることでターミナル作業が快適になります。

![cowsay](sample/cowsay/cowsay.gif)

# フォントにまつわるEAW問題
- 狭くなる
- 右端が切れる
- 重なる
- 重ならないがスペースの後置が必要

[locale-eaw](https://github.com/hamano/locale-eaw)とこのフォントの組み合わせによって上記の問題を修正します。

# 合成フォント

このフォントは現状下記フォントを合成していますが、
今後よりよいフォントがあれば入れ替えを行う可能性があります。

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

## EAW-CONSOLE
AmbiguousとNeutralの文字幅を個別に裁定

- 半角にしないとTUIが壊れる文字は半角(罫線・ブロック)
- 日本語圏で全角として扱われることが多い文字は全角(例※①)
- NerdFontのプライベート領域を全角
- 半角で描画することが困難な絵文字を全角

修正ロケール[EAW-CONSOLE](https://github.com/hamano/locale-eaw)に適合するフォントです。

## EAW-FULLWIDTH
- East Asian Width=Ambisious文字をすべて全角にしたフォント
- Ambisious Widthを全角に統一するしかない、古典的なアプリケーションに適応します。
- 罫線が全角となるのでTUIが壊れます。
- EAW=Nerutralな文字が半角となるので潰れる絵文字があります。
- ギリシャ文字やキリル文字が全角となります。

修正ロケール[EAW-FULLWIDTH](https://github.com/hamano/locale-eaw)に適合するフォントです。

### サンプル

![EAW-CONSOLEのサンプル画像](./sample/sample.png)

## イタリック体の再考

ターミナルではイタリック体やボールド体の修飾が可能です。
イタリック体は欧文であれば特徴的ですが、和文ではただの斜体となり識別性がよくありません。

そこで、このフォントのイタリック体は欧文でセリフ付きイタリック体、和文では明朝体の斜体にするという実験を行っています。

これにより和文でもイタリック体が区別しやすくなることを期待しています。

