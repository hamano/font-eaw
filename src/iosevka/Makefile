.PHONY: update

URL:=https://github.com/be5invis/Iosevka/releases/download/v31.6.1/
SRC:=PkgTTF-IosevkaTermCurly-31.6.1.zip PkgTTF-IosevkaTermCurlySlab-31.6.1.zip

update:
	@for f in $(SRC); do \
		curl -sL -w "%{http_code} $$f\n" --etag-save $$f.etag --etag-compare $$f.etag -o $$f ${URL}/$$f; \
	done

