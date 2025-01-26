.PHONY: update

URL:=https://github.com/be5invis/Iosevka/releases/download/v32.4.0/
SRC:=PkgTTF-IosevkaTermCurly-32.4.0.zip PkgTTF-IosevkaTermCurlySlab-32.4.0.zip

update:
	@for f in $(SRC); do \
		curl -sL -w "%{http_code} $$f\n" --etag-save $$f.etag --etag-compare $$f.etag -o $$f ${URL}/$$f; \
	done

