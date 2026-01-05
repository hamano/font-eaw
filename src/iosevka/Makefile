.PHONY: update

VER=34.0.0
URL:=https://github.com/be5invis/Iosevka/releases/download/v$(VER)/
SRC:=PkgTTF-IosevkaTermCurly-$(VER).zip PkgTTF-IosevkaTermCurlySlab-$(VER).zip

update:
	@for f in $(SRC); do \
		curl -sL -w "%{http_code} $$f\n" --etag-save $$f.etag --etag-compare $$f.etag -o $$f ${URL}/$$f; \
	done
	unzip -o PkgTTF-IosevkaTermCurly-$(VER).zip IosevkaTermCurly-Bold.ttf IosevkaTermCurly-Regular.ttf
	unzip -o PkgTTF-IosevkaTermCurlySlab-$(VER).zip IosevkaTermCurlySlab-BoldItalic.ttf IosevkaTermCurlySlab-Italic.ttf

